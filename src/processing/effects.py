
class Effect():

    def __init__(self):
        self.enable = True

    def set_perameter(self, **kwargs):

        for name, value in kwargs.items():
            if name not in self.parameters:
                raise ValueError(
                f"{name} is not a valid perameter"
                )

            self.parameters[name] = value
        

    def get_perameter():
        pass

    def enable(self):
        self.enable = True

    def bypass(self):
        self.enable = False