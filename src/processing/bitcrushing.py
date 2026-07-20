import numpy as np

class BitCrushing():

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.bit_depth = 10

    def process(self, audio):

        print("CALLING: bit crusher")
        return self.algorithm.process(audio, self.bit_depth)

class BitDepthReduction():

    def process(self, audio, bit_depth):
        print("RUNNING: bit depth reduction")
        np_audio = np.array(audio)
        np_audio = (np.round(np_audio * 2 **bit_depth)) / (2**bit_depth / 2)
        return np_audio

class FractinalBitCrush():

    def process():
        pass

