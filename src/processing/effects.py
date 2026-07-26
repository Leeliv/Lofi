
class Effect():

    def set_perameter(self, **kwargs):

        for name, value in kwargs.items():
            if name not in self.parameters:
                raise ValueError(
                f"{name} is not a valid perameter"
                )

            self.parameters[name] = value
        

    def get_perameter():
        pass