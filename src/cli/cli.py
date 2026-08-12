
from processing.softclipping import SoftClipping, CubeWave
from processing.bitcrushing import BitCrushing, BitDepthReduction
from processing.downsampling import DownSampler, ZeroAndHold
from processing.wowflutter import WowAndFlutter, LFO
from processing.delay import Delay, SimpleDelayBuffer
from processing.lowpassfilter import LpwPassFilter, lpf

class CLI():

    def __init__(self, audio_engin,command_queue):
        self.command_queue = command_queue
        self.audio_engin = audio_engin
        self.running = True
        self.effects = []

    def run(self):
        while self.running:
            print(*self.effects)
            command_string = input(">LOFI PEDAL \n")
            print("\n")
            command_split = command_string.split(" ")
            command = command_split[0]
            perameters = command_split[1:]

            if command == "add":
                command_obj = AddCommand(perameters)
                command_obj.build()
                self.effects.append(perameters[0])
                self.command_queue.put(command_obj)
            
            if command == "remove":
                command_obj = RemoveCommand(perameters[0])
                self.command_queue.put(command_obj)

            if command == "bypass":
                command_obj = BypassCommand(perameters[0])
                self.command_queue.put(command_obj)

            if command == "pause":
                command_obj = PauseCommand()
                self.command_queue.put(command_obj)

            if command == "play":
                command_obj = PlayCommand()
                self.command_queue.put(command_obj)

    def edit():
        pass

    def stop(self):
        self.running = False

class PlayCommand():

    def execute(self, engine):
        engine.resume()

class PauseCommand():

    def execute(self, engine):
        engine.pause()

class BypassCommand():

    def __init__(self, index):
        self.index = int(index)

    def execute(self, engine):
        engine.pedal.bypass_effect(self.index)


class RemoveCommand():
    
    def __init__(self, index):
        self.index = int(index)

    def execute(self, engine):
        engine.pedal.remove_effect(self.index)


class AddCommand():

    def __init__(self, perameters):
        self.effect = None
        self.perameters = perameters
        # self.effect_obj = None

    def build(self):
        # print("peramsssss")

        if not self.perameters:
            return

        if self.perameters[0] == "bit_crush":
            self.effect = BitCrushing(int(self.perameters[1]), BitDepthReduction())

        if self.perameters[0] == "soft_clip":
            self.effect = SoftClipping(int(self.perameters[1]), CubeWave())

        if self.perameters[0] == "delay":
            self.effect = Delay(SimpleDelayBuffer())

        if self.perameters[0] == "down_sample":
            self.effect = DownSampler(int(self.perameters[1]), ZeroAndHold())
            
        if self.perameters[0] == "wow_flutter":
            self.effect = WowAndFlutter(self.sample_rate, LFO())

        if self.perameters[0] == "lpf":
            self.effect = LpwPassFilter(float(self.perameters[1]), lpf())

    def execute(self, engine):
        engine.pedal.add_effect(self.effect)

