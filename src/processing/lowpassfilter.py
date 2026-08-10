import numpy as np

from processing.effects import Effect

class LpwPassFilter(Effect):

    def __init__(self, smooth_factor, algorithm):
        self.algorithm = algorithm
        self.smooth_factor = smooth_factor

    def process(self, audio):
        # print("CALLING: low pass filter")
        return self.algorithm.process(audio, self.smooth_factor)

class lpf():

    def __init__(self):
        self.prev_audio = np.full((1024,2),9)

    def process(self, audio, smooth_factor):
        #y[i] = alpha * x[i] + (1 - alpha) * y[i-1]
        if (self.prev_audio[1] == 9).any():
            
            self.prev_audio = audio
            return audio

        return smooth_factor * audio + (1 - smooth_factor) * self.prev_audio