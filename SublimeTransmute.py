import sublime
import sublime_plugin
import getopt
import re
import __future__

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        sublime.active_window().show_input_panel("Transmute Code", "gen 1 10", on_done, None, None)

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

    def reverse(self):
        return self.body[::-1]

    # def gen(self):
    #     return "\n".join(str(i) for i in range(1,10,2))

    def gen(self):

        # Option status
        prefix = ''
        suffix = ''
        range_start = 0
        range_end = 0
        range_increment = 1
        seperator = '\n'

        # Mutation Case Algorithms
        def default():
            return seperator.join((prefix+str(i)+suffix) for i in range(range_start,range_end,range_increment))

        # Option Parsing
        try:
            opts, args = getopt.getopt(self.params, 'b:a:s')
        except getopt.GetoptError as err:
            # will print something like "option -a not recognized"
            sublime.error_message("For command: '" + self.command_name + "'\n\n" + str(err))
            return self.body

        # Option Handling
        for o, a in opts:
            if o == "-s":
                seperator = ''
            elif o == "-b":
                prefix = a
            elif o == "-a":
                suffix = a

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
        newline = ''
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
            if o == "-l":
                newline = '\n'

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

