import websockets
import asyncio
import soundfile as sf
import numpy as np

async def send_file():
    url = "ws://localhost:8000/ws/process-wav"
    async with websockets.connect(url) as ws:
        audio, sample_rate = sf.read("audio/chillshite.wav")
        audio_bytes = np.ascontiguousarray(audio, dtype="<f4").tobytes()
        await ws.send(audio_bytes)
        response = await ws.recv()
        print("Server response:", response)

asyncio.run(send_file())

'''can not send whole audio bytes at once too big 
websockets.exceptions.ConnectionClosedError: received 1009 (message too big) 
frame with 27158356 bytes exceeds limit of 16777216 bytes; t
hen sent 1009 (message too big) frame with 27158356 bytes exceeds limit of 16777216 bytes