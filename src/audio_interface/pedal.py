
class PedalBoard():

    def __init__(self):
        self.effects = []
        # self.effect_names = []

    def process(self, audio):
        for effect in self.effects:
            if effect.enable:
                audio = effect.process(audio)

        return audio

    def add_effect(self, effect):
        self.effects.append(effect)

    def remove_effect(self, index):
        self.effects.pop(index)

    def set_effect_perameters(self, effect_index, **kwargs):
        self.effects[effect_index].set_perameters(**kwargs)

    def set_perameter(self, effect_index, peram, value):
        self.effects[effect_index].set_perameter(peram, value)

    def bypass_effect(self, effect_index):
        self.effects[effect_index].bypass()

    def enable_effect(self, effect_index):
        self.effects[effect_index].enable()

