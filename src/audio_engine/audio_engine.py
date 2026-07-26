import sounddevice as sd
import threading

class AudioEngine():

    def __init__(self, pedal):
        self.pedal = pedal
        self.audio = []
        self.current_frame = 0 
    
    def callback(self, outdata, frames, time, status):
        if status:
            print(status)

        remaining = len(self.audio) - self.current_frame
        chunk_size = min(remaining, frames)
        chunk = self.audio[self.current_frame: self.current_frame+chunk_size]
        chunk = self.pedal.process(chunk)

        if len(chunk) < frames:
            outdata[chunk_size:] = 0
            raise sd.CallbackStop()

        outdata[:] = chunk
        self.current_frame += chunk_size 
        
    def play(self, audio, sample_rate):
        finnished = threading.Event()
        self.audio = audio
        with sd.OutputStream(
            samplerate = sample_rate,
            # blocksize = blocksize,
            channels = 2,
            callback = self.callback,
            finished_callback = finnished.set
        ):
            finnished.wait()
            print("finnished")

