class SoftClipping():

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def process (self, audio):
        return self.algorithm.process(audio)

#Algorithm classes

class CubeWave():

    def process(self, audio):
        length = len(audio)
        clipped_audio = []

        for frame in audio:

            if frame[1] <= -1:
                res = (2/3) * -1
                clipped_audio.append([res, res])
                print(res)

            elif frame[1] >=  -1 and frame[1] <= 1:
                res = frame[1] - ((frame[1]**3) / 3)
                clipped_audio.append([res, res])
                print(res)

            elif frame[1] >= 1:
                res = 2/3
                clipped_audio.append([res,res])
                print(res)

        return clipped_audio

class PolyWave():

    def process(self, audio):
        return

class HyperbolicTan():

    def process(self, audio):
        return 