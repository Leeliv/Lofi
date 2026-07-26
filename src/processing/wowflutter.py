import numpy as np

class WowAndFlutter():

    def __init__(self, sample_rate, algorithm):
        self.algorithm = algorithm
        self.sample_rate = sample_rate
        self.wow_depth = 50
        self.wow_rate = 2
        self.flutter_depth = 20
        self.flutter_rate = 0.5 
        

    def process(self, audio):
        print("CALLING: wow and flutter")
        return self.algorithm.process(audio, self.sample_rate, self.wow_rate, self.wow_depth)

class LFO():

    def __init__(self):
        self.flutter_phase = 0
        self.wow_phase = 0

    def process(self, audio, sample_rate, wow_depth=20, wow_rate=0.5):
        print("RUNNING: LFO")
        output = np.zeros_like(audio)

        for i in range(len(audio)):
        # Time in seconds
            t = i / sample_rate

        # Create a slow tape-speed wobble
            flutter_wave = np.sin(2 * np.pi * 10 * t + self.flutter_phase) * 5
            # flutter_wave +=  np.sin(2 * np.pi * 8 * t) * 15
            wow_wave = np.sin(2 * np.pi * wow_rate * t + self.wow_phase) * wow_depth
            offset = flutter_wave + wow_wave

        # Move the read position
            read_position = i + offset

        # Keep it inside the buffer
            if read_position < 0:
                read_position = 0
            elif read_position >= len(audio) - 1:
                read_position = len(audio) - 2

        # Because read_position is a float, interpolate
            index = int(read_position)
            fraction = read_position - index

            output[i] = (
                audio[index] * (1 - fraction)
                + audio[index + 1] * fraction
            )

            self.flutter_phase += (
                2 * np.pi * 10 * len(audio) / sample_rate
            )
            self.wow_phase += (
                2 * np.pi * wow_rate * len(audio) / sample_rate
            )



        return output