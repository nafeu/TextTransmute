import sublime
import sublime_plugin
import re
from .commands import *

AVAILABLE_COMMANDS = [str(t).replace("<class 'SublimeTransmute.commands.", "")
                      .replace("'>", "")
                      .lower()
                      for t in globals().values()
                      if ('SublimeTransmute.commands.' in str(t)
                          and 'Test' not in str(t))]

# Sublime Text Plugin Commands

class SublimeTransmuteInitCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit):

        def on_done(text):
            self.view.run_command("sublime_transmute_parse",
                                  {"user_input": text})

        try:
            project_data = sublime.active_window().project_data()
            if 'history' in project_data.keys():
                input_field = project_data['history']
            else:
                input_field = ""
        except AttributeError:
            input_field = ""

        sublime.active_window().show_input_panel("Transmute Selection",
                                                 input_field,
                                                 on_done,
                                                 None,
                                                 None)


class SublimeTransmuteParseCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit, user_input):

        append_to_sel = False
        region_set = self.view.sel()
        error_logger = WindowErrorLogger()

        ws_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')

        def strip_quotes(input_string):
            if ((input_string[0] == input_string[len(input_string)-1])
                    and (input_string[0] in ('"', "'"))):
                return input_string[1:-1]
            return input_string

        def eval_simple_expr(input_string):
            if ((input_string[0] == input_string[len(input_string)-1])
                    and (input_string[0] in '`')):
                return eval_expr(input_string[1:-1])
            return input_string

        def clean_param(param):
            return str(eval_simple_expr(strip_quotes(param)))

        if user_input[0] == "+":
            to_parse = user_input[1:]
            append_to_sel = True
        else:
            to_parse = user_input

        command_list = [x.strip() for x in pipe_pattern.split(to_parse)[1::2]]
        for region in region_set:

            body = self.view.substr(region)

            for command in command_list:
                params = None
                # split incoming input into a list by delimiter whitespace
                input_split = [clean_param(x)
                               for x in ws_pattern.split(command)[1::2]]
                command_name = input_split[0]
                if input_split:
                    params = input_split[1:]
                if command_name.capitalize() in globals():
                    try:
                        transmutor = globals()[command_name.capitalize()](error_logger)
                        body = str(transmutor.transmute(body, params))
                    except Exception as e:
                        error_logger.display_error("Transmutation Error: '%s'",
                                                   str(e))
                        break
                else:
                    error_logger.display_error("Transmutation Error: '%s' is not a valid command",
                                               command)
                    raise InvalidTransmutation(command)
                if append_to_sel:
                    body = self.view.substr(region)+'\n\n'+body

            self.view.run_command("sublime_transmute_exec", {"region_begin" : region.begin(),
                                                             "region_end" : region.end(),
                                                             "string" : body})

        project_data = sublime.active_window().project_data()
        project_data['history'] = user_input
        sublime.active_window().set_project_data(project_data)


class SublimeTransmuteExecCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)


class SublimeTransmuteListCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit):

        def on_done(text):
            self.view.run_command("sublime_transmute_parse", {"user_input": text})

        def on_select(selected_index):
            sublime.active_window().show_input_panel("Transmute Selection",
                                                     AVAILABLE_COMMANDS[selected_index],
                                                     on_done,
                                                     None,
                                                     None)

        sublime.active_window().show_quick_panel(AVAILABLE_COMMANDS, on_select)


# Exception Handling

class WindowErrorLogger(object):
    """
    TODO: Add docstring...
    """
    def display_error(self, message):
        sublime.error_message(message)

class InvalidTransmutation(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
