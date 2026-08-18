import sounddevice as sd
import threading

import numpy as np
from queue import Queue, Empty

#EFFECTS
from processing.softclipping import SoftClipping, CubeWave
from processing.bitcrushing import BitCrushing, BitDepthReduction
from processing.downsampling import DownSampler, ZeroAndHold
from processing.wowflutter import WowAndFlutter, LFO
from processing.delay import Delay, SimpleDelayBuffer
from processing.lowpassfilter import LpwPassFilter, lpf

class AudioEngine():

    def __init__(self, sample_rate, pedal, command_queue):
        self.effect_list = {
            "soft_clip": ["drive: float"],
            "bit_crush": ["bit_depth: int"],
            "down_sample": ["reduction: int"],
            "wow_flutter": ["wow_depth: float", "wow_rate: float", "flutter_depth: float", "flutter_rate: float"],
            "delay": ["delay_time: Float", "feedback: Float"],
            "lpf": ["smooth_factor: int(0-1)"]
        }
        self.command_queue = command_queue
        self.pedal = pedal
        self.audio = []
        self.current_frame = 0 
        self.sample_rate = sample_rate
        self.playback = True
    
    def callback(self, outdata, frames, time, status):
        if status:
            print(status)

        self.process_command()

        if self.playback == False:
            outdata.fill(0)
        else:
            remaining = len(self.audio) - self.current_frame
            chunk_size = min(remaining, frames)
            chunk = self.audio[self.current_frame: self.current_frame+chunk_size]
            chunk = np.asarray(chunk, dtype=np.float32)
            chunk = self.pedal.process(chunk)

            if len(chunk) < frames:
                outdata[chunk_size:] = 0
                raise sd.CallbackStop()

            outdata[:] = chunk
            self.current_frame += chunk_size 

    def process_command(self):
        while True:
            try:
                command_obj = self.command_queue.get_nowait()
                command_obj.execute(self)

            except Empty:
                break
        
    def play(self, audio, sample_rate):
        finnished = threading.Event()
        self.audio = audio
        with sd.OutputStream(
            samplerate = sample_rate,
            channels = 2,
            callback = self.callback,
            finished_callback = finnished.set,
            blocksize = 1024
        ):
            finnished.wait()
            print("finnished")

    def pause(self):
        self.playback = False
        print("PAUSINGGGG")

    def resume(self):
        self.playback = True
        print("PLAYYYINGGG")

