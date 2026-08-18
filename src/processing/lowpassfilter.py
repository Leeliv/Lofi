import numpy as np

from processing.effects import Effect

class LpwPassFilter(Effect):

    def __init__(self, smooth_factor, algorithm):
        self.algorithm = algorithm
        self.parameters = {
            "smooth_factor": smooth_factor
        }

    def process(self, audio):
        # print("CALLING: low pass filter")
        return self.algorithm.process(audio, **self.parameters)

class lpf():

    def __init__(self):
        self.prev_audio = np.zeros(2, dtype = np.float32)

    def process(self, audio, smooth_factor):
        #y[i] = alpha * x[i] + (1 - alpha) * y[i-1]
        output = np.empty_like(audio, dtype=np.float32)

        for i, frame in enumerate(audio):
            output[i] = (smooth_factor * frame + (1 - smooth_factor) * self.prev_audio)
            self.prev_audio = output[i]

        # if (self.prev_audio[1] == 9).any():
            
        #     self.prev_audio = audio
        #     return audio

        return output