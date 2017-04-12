class Transmutation(object):
    def __init__(self, body):
        self.body = body
    def transmute(self):
        # Mutation Case Algorithms
        def default():
            return self.body

        # def other_cases():
        #     return len(self.body.split())

        # Option Parsing
        # try:
        #     opts, args = getopt.getopt(self.params, 'lws:')
        # except getopt.GetoptError as err:
        #     # will print something like "option -a not recognized"
        #     self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
        #     return self.body

        # # Option Handling
        # for o, a in opts:
        #     if o == "-l":
        #         return other_cases()

        # # Arg Handling
        # if args:
        #     multiplier = args[0]

        # default
        return default()
