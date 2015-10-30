import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        sublime.active_window().show_input_panel("Transmute Code", "length", on_done, None, None)

class ParseCommand(sublime_plugin.TextCommand):
    '''
    Parse Logic:
    '''
    def run(self, edit, user_input):
        region_set = self.view.sel()
        # command_list = user_input.split("|")
        command_list = [x.strip() for x in user_input.split('|')]
        # sublime.error_message(str(command_list))
        m = MutationEngine()

        for region in region_set:
            # grab the content of the region
            body = self.view.substr(region)
            for command in command_list:
                # go through each command and mutate it accordingly
                body = m.mutate(body, command)
            # call the transmutation to replace it on your screen
            print("OUTPUT BODY IS: " + body)
            self.view.run_command("transmute", {"region_begin" : region.begin(), "region_end" : region.end(), "string" : body})

    # def mutator(self, body, command_name):
    #     output = ""
    #     if (command_name == "length"):
    #         output = len(body)
    #     elif (command_name == "repeat"):
    #         output = body + body
    #     elif (command_name == "reverse"):
    #         output = body[::-1]
    #     else:
    #         print("Invalid transmutation command: '" + command_name + "'")
    #         return body
    #     return str(output)

class MutationEngine:

    def __init__(self):
        self.body = ""
        self.command_name = ""
        self.args = ""
        # list all the methods that are not default object methods
        self.command_lib = [
            method for method in dir(MutationEngine)
                if callable(getattr(MutationEngine, method))
                and ("__" not in method)
                and ("mutate" not in method)
        ]

    def mutate(self, body, command):
        self.body = body
        # also later consider splitting up the arguments here
        if command in self.command_lib:
            return str(eval("self."+command)())
        else:
            print("Invalid Command: " + command)
            return body

    def length(self):
        return len(self.body)

class TransmuteCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_begin, region_end, string):
        region = sublime.Region(region_begin, region_end)
        self.view.replace(edit, region, string)

'''

1. Input
2. Parse
3. Map to Command
4. Process Transmutation
5. Replace/Insert Text

'''

