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
        self.command_queue = command_queue
        self.pedal = pedal
        self.audio = []
        self.current_frame = 0 
        self.sample_rate = sample_rate
    
    def callback(self, outdata, frames, time, status):
        if status:
            print(status)

        self.process_command()

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
                command_obj.execute(self.pedal)

                # command = command_obj[0]
                # perameters = command_obj[1]

                # if command == "add":

                    # if not perameters:
                    #     break

                    # if perameters[0] == "bit_crush":
                    #     self.pedal.add_effect(BitCrushing(int(perameters[1]), BitDepthReduction()))
                    
                    # if perameters[0] == "soft_clip":
                    #     self.pedal.add_effect(SoftClipping(int(perameters[1]), CubeWave()))

                    # if perameters[0] == "delay":
                    #     self.pedal.add_effect(Delay(SimpleDelayBuffer()))

                    # if perameters[0] == "down_sample":
                    #     self.pedal.add_effect(DownSampler(int(perameters[1]), ZeroAndHold()))

                    # if perameters[0] == "wow_flutter":
                    #     self.pedal.add_effect(WowAndFlutter(self.sample_rate, LFO()))

                    # if perameters[0] == "lpf":
                    #     self.pedal.add_effect(LpwPassFilter(float(perameters[1]), lpf()))



            except Empty:
                break
        
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

