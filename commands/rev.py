from SublimeTransmute.commands.transmutation import Transmutation

class Rev(Transmutation):
    def transmute(self):
        # Mutation Case Algorithms
        def default():
            return self.body[::-1]

        def other_cases():
            return self.body + self.body

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.display_error("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-l":
                return other_cases()

        # Arg Handling
        if args:
            argument = args[0]

        # default
        return default()