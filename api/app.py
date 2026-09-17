# from fastapi import FastAPI, WebSocket

# #DS
# from queue import Queue

# #
# from audio_engine.audio_engine import AudioEngine
# from audio_interface.pedal import PedalBoard

# command_queue = Queue()
# pedal = PedalBoard()
# engine = AudioEngine(pedal, command_queue)

# app = FastAPI()

# app.state.engine = engine

# @app.websocket("/ws")
# async def ws_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     #data = await websocket.receive_bytes()

#     while True:
#         chunk 

# def get_next_processed_chunk():

"""WebSocket API for streaming processed WAV audio.

Send one complete WAV file as a binary WebSocket message to
``/ws/process-wav``. The server then sends an ``audio-start`` JSON message,
raw float32 PCM binary chunks, and an ``audio-end`` JSON message. Each
connection owns its own AudioEngine, so stateful effects do not leak between
clients.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from queue import Queue
import sys

import numpy as np
import soundfile as sf
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.concurrency import run_in_threadpool


# This repository keeps the application modules in ``src`` without packaging
# them as an installed distribution.  Make the API runnable with
# ``uvicorn api.app:app`` from the repository root.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from audio_engine.audio_engine import AudioEngine
from audio_interface.pedal import PedalBoard


app = FastAPI(title="Lofi Audio API")
CHUNK_FRAMES = 1024


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


@app.websocket("/ws/process-wav")
async def process_wav(websocket: WebSocket) -> None:
    """Receive full WAV uploads, then stream processed PCM frames back."""
    await websocket.accept()
    engine = AudioEngine(sample_rate=44_100, pedal=PedalBoard(), command_queue=Queue())

    try:
        while True:
            wav_bytes = await websocket.receive_bytes()
            try:
                audio, sample_rate = await run_in_threadpool(decode_wav_bytes, wav_bytes)
            except InvalidWavError as exc:
                await websocket.send_json({"error": str(exc)})
                continue
            except Exception:
                await websocket.send_json({"error": "Unable to process the WAV file."})
                continue

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
    except WebSocketDisconnect:
        pass
