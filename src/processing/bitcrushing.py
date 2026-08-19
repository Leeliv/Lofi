import numpy as np
from processing.effects import Effect

class BitCrushing(Effect):

    def __init__(self, bit_depth, algorithm):
        super().__init__()

        self.name = "bit_crush"
        self.algorithm = algorithm
        self.parameters = {
            "bit_depth": bit_depth
        }

    def process(self, audio):
        # print("CALLING: bit crusher")
        return self.mix(self.algorithm.process(audio, **self.parameters), audio)

class BitDepthReduction():

    def process(self, audio, bit_depth):
        # print("RUNNING: bit depth reduction")
        levels = 2 ** bit_depth
        np_audio = np.array(audio)
        # np_audio = (np.round(np_audio * 2 **bit_depth)) / (2**bit_depth / 2)
        
        np_audio = np.round(np_audio * levels) / levels

        return np_audio

class FractinalBitCrush():

    def process():
        pass

