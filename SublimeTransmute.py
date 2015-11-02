import sublime
import sublime_plugin
import getopt
import re
import __future__
from itertools import permutations

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print(sublime.active_window().project_data())
        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        project_data = sublime.active_window().project_data()
        if 'history' in project_data.keys():
            input_field = project_data['history']
        else:
            input_field = ""
        sublime.active_window().show_input_panel("Transmute Code", input_field, on_done, None, None)


class ParseCommand(sublime_plugin.TextCommand):

    def run(self, edit, user_input):
        error_status = False
        region_set = self.view.sel()
        pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        command_list = [x.strip() for x in pipe_pattern.split(user_input)[1::2]]
        m = MutationEngine()
        for region in region_set:
            # grab the content of the region
            body = self.view.substr(region)
            for command in command_list:
                # go through each command and mutate it accordingly
                try:
                    body = m.mutate(body, command)
                except InvalidTransmutation as e:
                    sublime.error_message("Invalid Transmutation Command: \n\n'" + e.value + "'")
                    error_status = True
                    break
                except SyntaxError as e:
                    sublime.error_message("Invalid Transmutation Syntax: \n\n'" + str(e) + "'")
                    error_status = True
                    break
                except NameError as e:
                    sublime.error_message("Invalid Transmutation Command: \n\n'" + str(e) + "'")
                    error_status = True
                    break
            # call the transmutation to replace it on your screen
            if not error_status:
                project_data = sublime.active_window().project_data()
                project_data['history'] = user_input
                sublime.active_window().set_project_data(project_data)
                # sublime.active_window().set_project_data()
                self.view.run_command("transmute", {"region_begin" : region.begin(), "region_end" : region.end(), "string" : body})

class MutationEngine:

    def __init__(self):
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

    def mutate(self, body, command):

        def strip_quotes(input_string):
            if (input_string[0] == input_string[len(input_string)-1]) and (input_string[0] in ('"',"'")):
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

    def clip(self):
        return sublime.get_clipboard()

    def rev(self):
        return self.body[::-1]

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
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
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
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
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
            return str(placement.replace('{$}',str(s)))

        # Option status
        placement = '{$}'
        range_start = 0
        range_end = 0
        range_increment = 1
        seperator = '\n'

        # Mutation Case Algorithms
        def default():
            return seperator.join(place(i, placement) for i in range(range_start, range_end, range_increment))

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'cs:')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-c":
                seperator = ''
            elif o == "-s":
                placement = a
                if not placement.find('{$}'):
                    placement = a + '{$}'

        # Arg Handling
        if len(args) >= 2:
            range_start = int(args[0])
            range_end = int(args[1]) + 1
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
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
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
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
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
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
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


class TransmuteCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)

# Helpers
class InvalidTransmutation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def simple_expr(expression):
    restrict_chars = (' ','+','-','/','*','^','%')
    back_ops = tuple('(') + restrict_chars
    fwd_ops = tuple(')') + restrict_chars
    x, i = expression, 0
    end_size = len(x)
    while (i < len(x)-1):
        if (i > 0):
            if x[i] == '(' and x[i-1] not in back_ops and x[i+1] not in fwd_ops:
                x = x[:i] + '*' + x[i:]
            elif x[i] == ')' and x[i-1] not in back_ops and x[i+1] not in fwd_ops:
                x = x[:i+1] + '*' + x[i+1:]
            elif x[i] == '^':
                x = x[:i] + '**' + x[i+1:]
            end_size += 1
            i += 1
        i += 1
    return eval(compile(x, '<string>', 'eval', __future__.division.compiler_flag))

'''

1. Input
2. Parse
3. Map to Command
4. Process Transmutation
5. Replace/Insert Text

'''

