import numpy as np

from processing.effects import Effect

#DSP
from processing.softclipping import CubeWave
from processing.lowpassfilter import lpf

class Delay(Effect):
    def __init__(self, algorithm):
        super().__init__()

        self.algorithm = algorithm
        self.perameters = {
        }

    def process(self, audio):
        return self.algorithm.process(audio)

class SimpleDelayBuffer():

    def __init__(self):
        self.buffer = [np.full((1024,2),9)] * 70
        self.buffer_index = 0
        self.saturartion = CubeWave()

    def process(self, audio):
        if self.buffer_index == len(self.buffer):

            #reset buffer index for circular array
            self.buffer_index %= len(self.buffer)

        print(self.buffer)

        if (self.buffer[self.buffer_index][0] != 9).any():
            #add quiet delay to played audio
            low_pass_filter = lpf()
            cube_wave_clipping = CubeWave()
            new_audio = cube_wave_clipping.process(audio, 1)
            new_audio = low_pass_filter.process(new_audio, 0.5)
            new_audio = new_audio + (self.buffer[self.buffer_index] *0.2)

            #quieter delay to write to buffer
            soft_audio = new_audio * 0.5

            #soft clipped delay for buffer
            soft_audio = self.saturartion.process(soft_audio,2)

            self.buffer[self.buffer_index] = audio + soft_audio

            self.buffer_index += 1
            return new_audio
        else:
            self.buffer[self.buffer_index] = audio
            self.buffer_index += 1
            return audio

