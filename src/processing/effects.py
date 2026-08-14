
class Effect():

    def __init__(self):
        self.enable = True
        self.mix_percent = 0.8

    def set_perameters(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self.parameters:
                raise ValueError(
                    f"{name} is not a valid perameter"
                )

            self.parameters[name] = value

    def set_perameter(self, peram_name, value):
        if peram_name not in self.parameters:
            raise ValueError(
                f"{name} is not a valid perameter"
            )
        
        self.parameters[peram_name] = value
        

    def get_perameter():
        pass

    def enable(self):
        self.enable = True

    def bypass(self):
        self.enable = not self.enable

    def mix(self, wet, dry):
        # print("RUNNING MIXXXXXXX")
        return dry * (1 - self.mix_percent) + wet * (self.mix_percent)

