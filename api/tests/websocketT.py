"""Manual smoke test for the /ws/process-wav protocol.

Sends the effect catalog request, adds/bypasses/sets/removes an effect, then
uploads a WAV file in chunks (rather than one giant message, which the
server would reject once it exceeds the ASGI message-size limit) and
collects the processed audio back.

Run the API first:
    uv run uvicorn api.app:app --reload
Then:
    uv run python api/tests/websocketT.py
"""

import asyncio
import json

import numpy as np
import soundfile as sf
import sounddevice as sd
import websockets

WS_URL = "ws://localhost:8000/ws/process-wav"
WAV_PATH = "audio/chillshite.wav"
UPLOAD_CHUNK_BYTES = 256 * 1024  # comfortably under the 16 MiB default ws message limit


async def send_command(ws, payload):
    await ws.send(json.dumps(payload))
    reply = json.loads(await ws.recv())
    print("<-", reply)
    return reply


async def upload_wav(ws, path):
    with open(path, "rb") as f:
        wav_bytes = f.read()

    await send_command(ws, {"type": "upload-start", "total_bytes": len(wav_bytes)})

    #itterate over audio file in chunks
    for start in range(0, len(wav_bytes), UPLOAD_CHUNK_BYTES):
        chunk = wav_bytes[start : start + UPLOAD_CHUNK_BYTES]
        await ws.send(chunk)
        reply = json.loads(await ws.recv())
        print("<-", reply)

    await ws.send(json.dumps({"type": "upload-end"}))

    audio_start = json.loads(await ws.recv())
    print("<-", audio_start)
    assert audio_start["type"] == "audio-start"

    total_frames = audio_start["total_frames"]
    channels = audio_start["channels"]
    chunks = []
    received_frames = 0

    #create a list of received chunks
    while received_frames < total_frames:
        pcm_bytes = await ws.recv()
        frame = np.frombuffer(pcm_bytes, dtype="<f4").reshape(-1, channels)
        chunks.append(frame)
        received_frames += len(frame)

    audio_end = json.loads(await ws.recv())
    print("<-", audio_end)
    assert audio_end["type"] == "audio-end"

    #create new audio file with chunks
    processed = np.concatenate(chunks, axis=0)
    sf.write("audio/chillshite_processed.wav", processed, audio_start["sample_rate"])
    print(f"Wrote audio/chillshite_processed.wav ({received_frames} frames)")


def play_audio():
    data, sample_rate = sf.read(audio/chillshite.wav)
    pass


async def main():
    async with websockets.connect(WS_URL, max_size=None) as ws:
        await send_command(ws, {"type": "catalog"})
        await send_command(ws, {"type": "add", "effect": "bit_crush", "args": [6]})
        await send_command(ws, {"type": "set", "index": 0, "param": "bit_depth", "value": 7})
        await send_command(ws, {"type": "bypass", "index": 0})
        await send_command(ws, {"type": "bypass", "index": 0})

        await upload_wav(ws, WAV_PATH)

        await send_command(ws, {"type": "remove", "index": 0})



if __name__ == "__main__":
    asyncio.run(main())
