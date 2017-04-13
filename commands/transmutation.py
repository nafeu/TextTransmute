import getopt
import unittest

class Transmutation(object):

    def __init__(self, error_module=None):
        self.body = None
        self.error_module = error_module
        self.command = self.__class__.__name__.lower()

    def display_error(self, message):
        if self.error_module:
            self.error_module.display_error(message)
        else:
            print(message)

    def transmute(self, body, params=None):
        self.body = body

        # Mutation Case Algorithms
        def default():
            return self.body

        def other_case():
            return self.body + self.body

        # Option Parsing
        try:
            opts, args = getopt.getopt(params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.display_error("Transmutation Error: " + str(err) + " for " + self.command)
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-l":
                return other_case()

        # Arg Handling
        if args:
            argument = args[0]

        # default
        return default()

class TestTransmutation(unittest.TestCase):

    def setUp(self):
        self.t = Transmutation()

    def test_default(self):
        self.assertEqual(self.t.transmute("asdf"), "asdf")

    def test_other_case(self):
        self.assertEqual(self.t.transmute("asdf", ['-l']), "asdfasdf")