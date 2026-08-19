
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
            print("PRINTING COMMAND")
            print(command)
            perameters = command_split[1:]
            print(perameters)

            if command == "add":
                command_obj = AddCommand(perameters)
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

            if command == "effect":
                command_obj = ViewEffect(perameters, self.effects)
                self.command_queue.put(command_obj)

            if command == "effects":
                command_obj = ViewEffects()
                self.command_queue.put(command_obj)

            if command == "set":
                command_obj = EditPerams(perameters)
                self.command_queue.put(command_obj)

            if command == "list":
                command_obj = AllEffects()
                self.command_queue.put(command_obj)


    def edit():
        pass

    def stop(self):
        self.running = False

class AllEffects():

    def execute(self, engine):
        print("EFFECTS LIST")
        for effect, params in engine.effect_list.items():
            print(f"{effect}:")
            for param in params:
                print(f"    {param}")

            print("\n")

class ViewEffect():

    def __init__(self, perameters, effects):
        self.index = int(perameters[0])
        self.effects = effects

    def execute(self, engine):
        effect_name = self.effects[self.index]
        parameters_names = engine.pedal.effects[self.index].parameters
        print("\n")
        print(effect_name)
        print(parameters_names)
        print("\n")

class ViewEffects():

    def execute(self, engine):
        for i, effect in enumerate(engine.pedal.effects):
            print(f"{effect.name}: \n {effect.parameters} \n")


class EditPerams():

    def __init__(self, params):
        self.index = int(params[0])
        self.peram = params[1]
        self.value = float(params[2])
    
    def execute(self, engine):
        engine.pedal.set_perameter(self.index, self.peram, self.value)

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
        self.perameters = perameters

    def execute(self, engine):

        if not self.perameters:
            return 

        elif self.perameters[0] == "bit_crush":
            effect = BitCrushing(
                int(self.perameters[1]), 
                BitDepthReduction()
            )

        elif self.perameters[0] == "soft_clip":
            effect = SoftClipping(
                float(self.perameters[1]), 
                CubeWave()
            )

        elif self.perameters[0] == "delay":
            effect = Delay(
                SimpleDelayBuffer(engine.sample_rate)
            )

        elif self.perameters[0] == "down_sample":
            effect = DownSampler(
                int(self.perameters[1]), 
                ZeroAndHold()
            )
            
        elif self.perameters[0] == "wow_flutter":
            effect = WowAndFlutter(
                engine.sample_rate, 
                LFO()
            )

        elif self.perameters[0] == "lpf":
            effect = LpwPassFilter(
                float(self.perameters[1]), 
                lpf()
            )

        else:
            return 

        

        engine.pedal.add_effect(effect)

