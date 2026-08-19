import numpy as np

from processing.effects import Effect

class DownSampler(Effect):

    def __init__(self, reduction, algorithm):
        super().__init__()

        self.name = "down_sample"
        self.algorithm = algorithm
        self.parameters = {
            "reduction": reduction
        }

    def process(self, audio):
        # print("CALLING: down sampler")
        return self.algorithm.process(audio, **self.parameters)

class ZeroAndHold():

    def process(self, audio, reduction):
        # print("RUNNING: zero and hold")
        current = 0
        count = 0
        new_audio = np.empty_like(audio, dtype=np.float32)

        for i, sample in enumerate(audio):
            if count <= reduction:
                new_audio[i] = [current, current]
            else:
                current = sample[1]
                new_audio[i] = [current, current]
                count = 0
            count += 1

        return new_audio
