import getopt
import re

class Transmutation(object):

    def __init__(self, body, params, error_module):
        self.body = body
        self.params = params
        self.error_module = error_module
        self.command = self.__class__.__name__.lower()

    def transmute(self):
        # Mutation Case Algorithms
        def default():
            return self.body

        def other_cases():
            return self.body + self.body

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.display_error("For command: '" + self.command + "'\n\n" + str(err))
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
