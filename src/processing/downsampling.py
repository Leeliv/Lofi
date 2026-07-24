

class DownSampler():

    def __init__(self, reduction, algorithm):
        self.algorithm = algorithm
        self.reduction = reduction

    def process(self, audio):
        print("CALLING: down sampler")
        return self.algorithm.process(audio, self.reduction)

class ZeroAndHold():

    def process(self, audio, reduction):
        print("RUNNING: zero and hold")
        current = 0
        count = 0
        new_audio = []

        for sample in audio:

            if count <= reduction:
                new_audio.append([current, current])
            else:
                current = sample[1]
                new_audio.append([current, current])
                count = 0
            
            count +=1
            
        return new_audio
