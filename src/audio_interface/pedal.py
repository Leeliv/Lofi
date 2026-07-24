
class PedalBoard():

    def __init__(self):
        self.effects = []

    def process(self, audio):
        pro_audio = []
        for effect in self.effects:
            pro_audio = effect.process(audio)

        return pro_audio

    def add_effect(self, effect):
        self.effects.append(effect)

