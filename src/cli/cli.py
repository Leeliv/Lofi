
class CLI():

    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.running = True

    def run(self):
        while self.running:
            command_string = input(">LOFI PEDAL \n")
            command_split = command_string.split(" ")
            command = command_split[0]
            perameters = command_split[1:]

            if command == "add":
                self.add(perameters)

    def add(self, perameters):
        self.command_queue.put(["add", perameters])

    def remove():
        pass

    def bypass():
        pass

    def edit():
        pass

    def stop():
        pass

