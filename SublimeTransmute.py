import sublime
import sublime_plugin
import getopt

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        sublime.active_window().show_input_panel("Transmute Code", "dupl", on_done, None, None)

class ParseCommand(sublime_plugin.TextCommand):

    def run(self, edit, user_input):
        error_status = False
        region_set = self.view.sel()
        command_list = [x.strip() for x in user_input.split('|')]
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
        self.body = body
        # split incoming input into a list by delimiter whitespace
        input_split = command.split()
        # the first item in the list is your command name
        self.command_name = input_split[0]
        # the rest of the string is params
        if len(input_split) > 1:
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

class InvalidTransmutation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

'''

1. Input
2. Parse
3. Map to Command
4. Process Transmutation
5. Replace/Insert Text

'''

