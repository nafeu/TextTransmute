import getopt
import re
from itertools import permutations
from helpers import *
# import sublime

class MutationEngine:

    def __init__(self, error_module=None):
        self.body = ""
        self.command_name = ""
        self.params = ""
        # list all the methods that are not default object methods
        self.command_lib = [
            method for method in dir(MutationEngine)
            if callable(getattr(MutationEngine, method))
            and ("__" not in method)
            and ("mutate" not in method)
        ]
        if error_module:
            self.error_module = error_module
        else:
            error_logger = ConsoleErrorLogger()
            self.error_module = error_logger

    def mutate(self, body, command):
        # Helpers

        def strip_quotes(input_string):
            if (input_string[0] == input_string[len(input_string)-1]) and (input_string[0] in ('"', "'")):
                return input_string[1:-1]
            return input_string

        def eval_simple_expr(input_string):
            if (input_string[0] == input_string[len(input_string)-1]) and (input_string[0] in ('`')):
                return simple_expr(input_string[1:-1])
            return input_string

        def clean_param(param):
            return str(eval_simple_expr(strip_quotes(param)))

        self.body = body
        # split incoming input into a list by delimiter whitespace
        whitespace_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        input_split = [clean_param(x) for x in whitespace_pattern.split(command)[1::2]]
        # the first item in the list is your command name
        self.command_name = input_split[0]
        # the rest of the string is params
        if input_split:
            self.params = input_split[1:]

        if self.command_name in self.command_lib:
            return str(eval("self."+self.command_name)())
        else:
            raise InvalidTransmutation(command)

    # Mutation Methods --- ADD NEW METHODS HERE

    # def clip(self):
    #     # return 'CLIPBOARD GOES HERE'
    #     # root = Tkinter.Tk()
    #     # keep the window from showing
    #     # root.withdraw()
    #     # read the clipboard
    #     # return root.clipboard_get()
    #     # return sublime.get_clipboard()

    def rev(self):
        return self.body[::-1]

    def expr(self):

        # Mutation Case Algorithms
        def default():
            return simple_expr(self.body)

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        # for o, a in opts:
        #     if o == "-l":
        #         return other_cases()

        # Arg Handling
        # if args:
        #     multiplier = args[0]

        # default
        return default()

    def perms(self):

        # Mutation Case Algorithms
        def default():
            if len(self.body) > 6:
                raise InvalidTransmutation("'perms' input too big for this dinky plugin")
            else:
                return '\n'.join(i for i in set([''.join(p) for p in permutations(self.body)]))

        # Option Status
        to_permute = ""

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        # for o, a in opts:
        #     if o == "-l":
        #         return other_cases()

        # Arg Handling
        # if args:
        #     if len(args[0]) > 5:
        #         raise InvalidTransmutation("'perms' input too big for this dinky plugin")
        #     else:
        #         to_permute = args[0]
        # else:
        #     raise InvalidTransmutation("'swap' command needs arguments")

        # default
        return default()

    def swap(self):

        # Mutation Case Algorithms
        def default():
            return self.body.replace(old_string, new_string)

        def other_cases():
            return len(self.body.split())

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, '')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        # for o, a in opts:
        #     if o == "-l":
        #         return other_cases()

        # Arg Handling
        if len(args) > 1:
            old_string = args[0]
            new_string = args[1]
        else:
            raise InvalidTransmutation("'swap' command needs arguments")

        # default
        return default()

    def gen(self):

        # Helpers
        def place(s, placement):
            return str(placement.replace('{$}', str(s)))

        # Option status
        placement = '{$}'
        range_start = 0
        range_end = 0
        range_increment = 1
        seperator = '\n'
        alphabet = False

        # Mutation Case Algorithms
        def default():
            if alphabet:
                return seperator.join(place(chr(i), placement) for i in range(range_start, range_end, range_increment))
            return seperator.join(place(i, placement) for i in range(range_start, range_end, range_increment))

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'cs:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-c":
                seperator = ''
            elif o == "-s":
                placement = a
                if placement.find('{$}') == -1:
                    placement = a + '{$}'

        # Arg Handling
        if len(args) >= 2:
            try:
                range_start = int(args[0])
                range_end = int(args[1]) + 1
            except ValueError:
                range_start = ord(args[0])
                range_end = ord(args[1]) + 1
                alphabet = True
            try:
                range_increment = int(args[2])
            except IndexError:
                pass
            if range_start > range_end:
                range_increment *= -1
                range_end -= 2
        else:
            raise InvalidTransmutation("'gen' command needs arguments")

        # default
        return default()

    def count(self):

        # Mutation Case Algorithms
        def default():
            return len(self.body)

        def word_count():
            return len(self.body.split())

        def line_count():
            return self.body.count('\n')+1

        def string_count(input):
            return self.body.count(input)

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-l":
                return line_count()
            elif o == "-w":
                return word_count()
            elif o == "-s":
                return string_count(a)
            else:
                return default()

        # default
        return default()

    def dupl(self):

        # Option status
        newline = '\n'
        multiplier = 2

        # Mutation Case Algorithms
        def default():
            return ((self.body + newline) * int(multiplier))

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'l')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-s":
                newline = ''

        # Arg Handling
        if args:
            multiplier = args[0]

        # default
        return default()

    def arash(self):
        return "beck"

    '''
    COMMAND BUILDING TEMPLATE

    def template(self):

        # Mutation Case Algorithms
        def default():
            return len(self.body)

        def other_cases():
            return len(self.body.split())

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'lws:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            self.error_module.displayError("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-l":
                return other_cases()

        # Arg Handling
        if args:
            multiplier = args[0]

        # default
        return default()
    '''