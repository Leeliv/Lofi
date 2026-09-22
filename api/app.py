"""WebSocket API for streaming processed WAV audio.

Protocol on ``/ws/process-wav`` (one connection = one AudioEngine, so
stateful effects never leak between clients):

Text (JSON) messages, client -> server
    {"type": "catalog"}
        -> {"type": "catalog", "effects": {...}}
    {"type": "add", "effect": "bit_crush", "args": [6]}
    {"type": "remove", "index": 0}
    {"type": "bypass", "index": 0}
    {"type": "set", "index": 0, "param": "drive", "value": 3}
        -> {"type": "state", "chain": [...]}  (or {"type": "error", ...})
    {"type": "upload-start", "total_bytes": 123456}
        -> {"type": "upload-ack"}
    <binary WAV chunks, any size/number, sent after upload-start>
        -> {"type": "upload-progress", "received": N, "total": total_bytes}
    {"type": "upload-end"}
        -> {"type": "audio-start", ...}, binary PCM chunks, {"type": "audio-end"}

Uploads are chunked on purpose: a single oversized WebSocket message would
be rejected by the ASGI server's message-size limit long before it reached
this handler, so large files are sent as many small binary frames between
``upload-start`` and ``upload-end`` instead of one giant message.
"""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from queue import Queue
import sys
from types import SimpleNamespace

import numpy as np
import soundfile as sf
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool


# This repository keeps the application modules in ``src`` without packaging
# them as an installed distribution.  Make the API runnable with
# ``uvicorn api.app:app`` from the repository root.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from audio_engine.audio_engine import AudioEngine
from audio_interface.pedal import PedalBoard
from cli.cli import AddCommand, BypassCommand, EditPerams, RemoveCommand


app = FastAPI(title="Lofi Audio API")
CHUNK_FRAMES = 1024

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/ui", StaticFiles(directory=STATIC_DIR, html=True), name="ui")


class InvalidWavError(ValueError):
    """Raised when an upload cannot be decoded as a WAV file."""


def decode_wav_bytes(wav_bytes: bytes) -> tuple[np.ndarray, int]:
    """Decode a complete WAV upload into stereo float32 frames.

    The pedal algorithms expect stereo frames. Mono uploads are duplicated to
    stereo, while files with more than two channels are rejected explicitly.
    """
    try:
        if sf.info(BytesIO(wav_bytes)).format != "WAV":
            raise InvalidWavError("Upload must be a valid WAV file.")
        audio, sample_rate = sf.read(BytesIO(wav_bytes), dtype="float32", always_2d=True)
    except (RuntimeError, ValueError) as exc:
        raise InvalidWavError("Upload must be a valid WAV file.") from exc

    if audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)
    elif audio.shape[1] != 2:
        raise InvalidWavError("Only mono or stereo WAV files are supported.")

    return audio, sample_rate


def get_chain_state(engine: AudioEngine) -> list[dict]:
    """Serialize the engine's current effect chain for the frontend."""
    return [
        {
            "index": index,
            "name": effect.name,
            "enabled": bool(effect.enable),
            "parameters": dict(effect.parameters),
        }
        for index, effect in enumerate(engine.pedal.effects)
    ]


async def process_uploaded_wav(engine: AudioEngine, websocket: WebSocket, wav_bytes: bytes) -> None:
    """Decode a fully-assembled WAV upload and stream processed PCM back."""
    try:
        audio, sample_rate = await run_in_threadpool(decode_wav_bytes, wav_bytes)
    except InvalidWavError as exc:
        await websocket.send_json({"type": "error", "message": str(exc)})
        return
    except Exception:
        await websocket.send_json({"type": "error", "message": "Unable to process the WAV file."})
        return

    engine.sample_rate = sample_rate
    await websocket.send_json(
        {
            "type": "audio-start",
            "sample_rate": sample_rate,
            "channels": audio.shape[1],
            "format": "float32le",
            "chunk_frames": CHUNK_FRAMES,
            "total_frames": len(audio),
        }
    )

    for start in range(0, len(audio), CHUNK_FRAMES):
        processed = await run_in_threadpool(
            engine.process_audio, audio[start : start + CHUNK_FRAMES]
        )
        pcm_chunk = np.ascontiguousarray(processed, dtype="<f4").tobytes()
        await websocket.send_bytes(pcm_chunk)

    await websocket.send_json({"type": "audio-end"})


async def handle_command(engine: AudioEngine, websocket: WebSocket, payload: dict) -> None:
    """Run an add/remove/bypass/set command and reply with the new chain state."""
    msg_type = payload["type"]
    try:
        if msg_type == "add":
            name = payload.get("effect")
            if name not in engine.effect_list:
                raise ValueError(
                    f"Unknown effect {name!r}. Known effects: {sorted(engine.effect_list)}"
                )
            args = payload.get("args", [])
            perameters = [str(name)] + [str(arg) for arg in args]
            AddCommand(perameters).execute(engine)

        elif msg_type == "remove":
            RemoveCommand(payload["index"]).execute(engine)

        elif msg_type == "bypass":
            BypassCommand(payload["index"]).execute(engine)

        elif msg_type == "set":
            EditPerams([payload["index"], payload["param"], payload["value"]]).execute(engine)

    except (KeyError, IndexError, ValueError, TypeError) as exc:
        message = str(exc) or f"Invalid {msg_type!r} request."
        await websocket.send_json({"type": "error", "message": message})
        return

    await websocket.send_json({"type": "state", "chain": get_chain_state(engine)})


async def handle_text_message(engine: AudioEngine, websocket: WebSocket, upload: SimpleNamespace, text: str
) -> None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        await websocket.send_json({"type": "error", "message": "Invalid JSON message."})
        return

    if not isinstance(payload, dict) or "type" not in payload:
        await websocket.send_json(
            {"type": "error", "message": "Message must be a JSON object with a 'type' field."}
        )
        return

    msg_type = payload["type"]

    if msg_type == "catalog":
        await websocket.send_json({"type": "catalog", "effects": engine.effect_list})
        return

    #run when before receiving bytes
    if msg_type == "upload-start":
        upload.buffer = bytearray()
        upload.expected = payload.get("total_bytes")
        await websocket.send_json({"type": "upload-ack"})
        return

    #run after all bytes are received to then process
    if msg_type == "upload-end":
        if upload.buffer is None:
            await websocket.send_json(
                {"type": "error", "message": "No upload in progress. Send 'upload-start' first."}
            )
            return
        wav_bytes = bytes(upload.buffer)
        #reset buffer and expected
        upload.buffer = None
        upload.expected = None
        #process riceved bytes
        await process_uploaded_wav(engine, websocket, wav_bytes)
        return

    if msg_type in {"add", "remove", "bypass", "set"}:
        await handle_command(engine, websocket, payload)
        return

    await websocket.send_json({"type": "error", "message": f"Unknown message type: {msg_type!r}"})


async def handle_binary_chunk(websocket: WebSocket, upload: SimpleNamespace, data: bytes) -> None:
    if upload.buffer is None:
        await websocket.send_json(
            {
                "type": "error",
                "message": "Received binary data outside of an upload. Send 'upload-start' first.",
            }
        )
        return

    upload.buffer.extend(data)
    await websocket.send_json(
        {"type": "upload-progress", "received": len(upload.buffer), "total": upload.expected}
    )


@app.websocket("/ws/process-wav")
async def process_wav(websocket: WebSocket) -> None:
    """Accept JSON effect commands and chunked WAV uploads on one socket."""
    await websocket.accept()
    engine = AudioEngine(sample_rate=44_100, pedal=PedalBoard(), command_queue=Queue())
    upload = SimpleNamespace(buffer=None, expected=None)

    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                break

            #text is either a command or a message to setup/finnish tasks
            text = message.get("text")
            #data is when bytes are being recieved
            data = message.get("bytes")

            if text is not None:
                await handle_text_message(engine, websocket, upload, text)
            elif data is not None:
                await handle_binary_chunk(websocket, upload, data)
    except WebSocketDisconnect:
        pass
