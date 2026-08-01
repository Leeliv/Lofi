import numpy as np

from processing.effects import Effect

class DownSampler(Effect):

    def __init__(self, reduction, algorithm):
        self.algorithm = algorithm
        self.parameters = {
            "reduction": reduction
        }

    def process(self, audio):
        print("CALLING: down sampler")
        return self.algorithm.process(audio, **self.parameters)

class ZeroAndHold():

    def process(self, audio, reduction):
        print("RUNNING: zero and hold")
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

        # for sample in audio:

        #     if count <= reduction:
        #         # new_audio.append([current, current])
        #         np.append(new_audio, [current, current])
        #     else:
        #         current = sample[1]
        #         # new_audio.append([current, current])
        #         np.append(new_audio, [current, current])
        #         count = 0
            
        #     count +=1
            
        print(new_audio)
        return new_audio
