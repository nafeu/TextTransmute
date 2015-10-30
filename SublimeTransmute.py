import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        sublime.active_window().show_input_panel("Transmute Code", "length", on_done, None, None)

class ParseCommand(sublime_plugin.TextCommand):

    def run(self, edit, user_input):
        error_status = False
        region_set = self.view.sel()
        # command_list = user_input.split("|")
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
            raise InvalidTransmutation(command)

    # Mutation Methods --- ADD NEW METHODS HERE

    def clip(self):
        return sublime.get_clipboard()

    def length(self):
        return len(self.body)

    def repeat(self):
        return self.body + self.body


    def reverse(self):
        return self.body[::-1]


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

