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
            "feedback": 0.3
        }

    def process(self, audio):
        return self.algorithm.process(audio, **self.parameters)

class SimpleDelayBuffer():

    def __init__(self, sample_rate):

        self.sample_rate = sample_rate
        # self.buffer = [np.full((1024,2),9)] * 70
        self.saturartion = CubeWave()
        self.low_pass_filter = lpf()

        self.max_delay = 2.0
        self.buffer_size = 86

        self.buffer = np.zeros((self.buffer_size, 1024, 2), dtype=np.float32)
        self.buffer_index = 0

        # self.delay_sample = self.delay_time * sample_rate

    def process(self, audio, delay_time, feedback):
        #delay_time (seconds) is used to translate that into aproximate location in buffer for delay
        delay_sample = delay_time * self.sample_rate/1024
        read_index= (round(self.buffer_index - delay_sample)) % self.buffer_size

        #combines the new audio with pas audio to create echo effect
        new_audio = audio + (self.buffer[read_index] * feedback)
        

        #applies filters to current audio which will be used for the next feedback
        soft_audio = new_audio * 0.5
        soft_audio = self.low_pass_filter.process(audio, 0.2)
        soft_audio = self.saturartion.process(soft_audio,2)

        #writes the new audio with new echo to the buffer for next callback
        self.buffer[self.buffer_index] = audio + soft_audio

        #incerements the buffer andd keepsit circular
        self.buffer_index = (self.buffer_index + 1) % len(self.buffer)

        return new_audio
        

