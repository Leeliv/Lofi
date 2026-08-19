import numpy as np
from processing.effects import Effect

class SoftClipping(Effect):

    def __init__(self, drive, algorithm):
        super().__init__()
        self.name = "soft_clip"
        self.algorithm = algorithm
        self.parameters = {
            "drive": drive
        }

    def process (self, audio):
        # print("CALLING: soft clipping")
        # audio *= self.drive
        return self.algorithm.process(audio, **self.parameters)

#Algorithm classes

class CubeWave():

    def process(self, audio, drive):
        # print("RUNNING: cube wave")
        length = len(audio)
        clipped_audio = np.empty_like(audio, dtype=np.float32)

        audio *= drive

        for i, frame in enumerate(audio):

            if frame[1] <= -1:
                res = (2/3) * -1

            elif frame[1] >=  -1 and frame[1] <= 1:
                res = frame[1] - ((frame[1]**3) / 3)

            elif frame[1] >= 1:
                res = 2/3

            clipped_audio[i] = [res,res]

        return clipped_audio

class PolyWave():

    def process(self, audio):
        return

class HyperbolicTan():

    def process(self, audio):
        return 