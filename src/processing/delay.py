import numpy as np

from processing.effects import Effect

#DSP
from processing.softclipping import CubeWave
from processing.lowpassfilter import lpf

class Delay(Effect):
    def __init__(self, algorithm):
        super().__init__()

        self.algorithm = algorithm
        # self.sample_rate = sample_rate
        self.parameters = {
            "delay_time": 0.5,
            "feedback": 0.5
        }

    def process(self, audio):
        return self.algorithm.process(audio, **self.parameters)

class SimpleDelayBuffer():

    def __init__(self, sample_rate):

        self.sample_rate = sample_rate
        # self.buffer = [np.full((1024,2),9)] * 70
        self.saturartion = CubeWave()

        self.max_delay = 2.0
        self.buffer_size = 86

        self.buffer = np.zeros((self.buffer_size, 1024, 2), dtype=np.float32)
        self.buffer_index = 0

        # self.delay_sample = self.delay_time * sample_rate

    def process(self, audio, delay_time, feedback):
        # if self.buffer_index == len(self.buffer):

        #     #reset buffer index for circular array
        #     self.buffer_index %= len(self.buffer)

        # print(self.buffer)
        delay_sample = delay_time * self.sample_rate

        read_index= (self.buffer_index - delay_sample) % self.buffer_size
        
        # if (self.buffer[self.buffer_index][0] != 0).any():
            
            #Additinal effect algorithms
        low_pass_filter = lpf()
        cube_wave_clipping = CubeWave()
        new_audio = cube_wave_clipping.process(audio, 1)
        new_audio = low_pass_filter.process(new_audio, 0.5)

            #add quiet delay to played audio
        new_audio = new_audio + (self.buffer[self.buffer_index] * feedback)

            #quieter delay to write to buffer
        soft_audio = new_audio * 0.5

            #soft clipped delay for buffer
        soft_audio = self.saturartion.process(soft_audio,2)

        self.buffer[self.buffer_index] = audio + soft_audio

        self.buffer_index = (self.buffer_index + 1) % len(self.buffer)

        return new_audio
        

