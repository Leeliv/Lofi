
class PedalBoard():

    def __init__(self):
        self.effects = []

    def process(self, audio):
        pro_audio = audio
        for effect in self.effects:
            pro_audio = effect.process(pro_audio)

        return pro_audio

    def add_effect(self, effect):
        self.effects.append(effect)

    def set_effect_perameter(self, effect_index, **kwargs):
        self.effects[effect_index].set_perameter(**kwargs)

