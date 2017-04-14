import sublime
import sublime_plugin
import re
import getopt
from .commands import *

class SublimeTransmuteCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(text):
            self.view.run_command("parse", {"user_input": text})

        # command history persistence
        try:
            project_data = sublime.active_window().project_data()
            if 'history' in project_data.keys():
                input_field = project_data['history']
            else:
                input_field = ""
        except AttributeError:
            input_field = ""

        sublime.active_window().show_input_panel("Transmute Selection", input_field, on_done, None, None)


class ParseCommand(sublime_plugin.TextCommand):

    def run(self, edit, user_input):

        append_to_sel = False
        region_set = self.view.sel()
        error_logger = WindowErrorLogger()

        whitespace_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')

        if user_input[0] == "+":
            to_parse = user_input[1:]
            append_to_sel = True
        else:
            to_parse = user_input

        command_list = [x.strip() for x in pipe_pattern.split(to_parse)[1::2]]
        for region in region_set:
            # grab the content of the region
            body = self.view.substr(region)

            for command in command_list:

                params = None

                # split incoming input into a list by delimiter whitespace
                input_split = [x for x in whitespace_pattern.split(command)[1::2]]
                command_name = input_split[0]
                if input_split:
                    params = input_split[1:]

                # TODO: check to see if the command exists, else raise invalid transmutation
                if command_name.capitalize() in globals():
                    try:
                        transmutor = globals()[command_name.capitalize()](error_logger)
                        body = str(transmutor.transmute(body, params))
                    except Exception as e:
                        error_logger.display_error("Transmutation Error: '" + str(e) + "'")
                        break
                else:
                    error_logger.display_error("Transmutation Error: '" + command + "' is not a valid command")
                    raise InvalidTransmutation(command)

                if append_to_sel:
                    body = self.view.substr(region)+'\n\n'+body

            self.view.run_command("transmute", {"region_begin" : region.begin(),
                                                  "region_end" : region.end(),
                                                  "string" : body})

        project_data = sublime.active_window().project_data()
        project_data['history'] = user_input
        sublime.active_window().set_project_data(project_data)


class TransmuteCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)

# Plugin Specific Helper Classes

class WindowErrorLogger:

    def display_error(self, message):
        sublime.error_message(message)

# Exception Classes

class InvalidTransmutation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)