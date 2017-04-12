from SublimeTransmute.commands.transmutation import Transmutation

class Rev(Transmutation):
    def transmute(self):
        return self.body[::-1]