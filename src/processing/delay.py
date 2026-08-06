import numpy as np

from processing.effects import Effect

#DSP
from processing.softclipping import CubeWave

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
            self.buffer_index %= len(self.buffer)

        print(self.buffer)

        if (self.buffer[self.buffer_index][0] != 9).any():
            new_audio = audio + (self.buffer[self.buffer_index] *0.2)
            soft_audio = new_audio * 0.5

            self.buffer[self.buffer_index] = audio + (self.saturartion.process(soft_audio, 2))
            self.buffer_index += 1
            return new_audio
        else:
            self.buffer[self.buffer_index] = audio
            self.buffer_index += 1
            return audio

class SimpleCircularDelay():
    
    def process():
        pass
