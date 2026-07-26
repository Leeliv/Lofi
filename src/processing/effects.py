
class Effect():

    def set_perameter(self, name, value):
        if name not in self.parameters:
            raise ValueError(
                print(f"{name} is not a valid perameter")
            )

        self.parameters[name] = value
        

    def get_perameter():
        pass