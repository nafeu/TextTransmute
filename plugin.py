import sublime
import sublime_plugin
import re
import getopt
import __future__
from .commands import *

AVAILABLE_COMMANDS = [str(x).replace("<class 'SublimeTransmute.commands.", "")
                            .replace("'>", "")
                            .lower()
                            for x in globals().values()
                            if ('SublimeTransmute.commands.' in str(x)
                            and 'Test' not in str(x))]

# Sublime Text Plugin Commands

class SublimeTransmuteInitCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(text):
            self.view.run_command("sublime_transmute_parse", {"user_input": text})

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


class SublimeTransmuteParseCommand(sublime_plugin.TextCommand):

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

            self.view.run_command("sublime_transmute_exec", {"region_begin" : region.begin(),
                                                                "region_end" : region.end(),
                                                                "string" : body})

        project_data = sublime.active_window().project_data()
        project_data['history'] = user_input
        sublime.active_window().set_project_data(project_data)


class SublimeTransmuteExecCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)

class SublimeTransmuteListCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(text):
            self.view.run_command("sublime_transmute_parse", {"user_input": text})

        def on_select(selected_index):
            sublime.active_window().show_input_panel("Transmute Selection", AVAILABLE_COMMANDS[selected_index], on_done, on_cancel, None)

        def on_cancel():
            project_data['history'] = ""
            sublime.active_window().set_project_data(project_data)

        sublime.active_window().show_quick_panel(AVAILABLE_COMMANDS, on_select)


# Helpers

class WindowErrorLogger:

    def display_error(self, message):
        sublime.error_message(message)


def simple_expr(expression):
    restrict_chars = (' ','+','-','/','*','^','%')
    back_ops = tuple('(') + restrict_chars
    fwd_ops = tuple(')') + restrict_chars
    x, i = expression, 0
    x = "("+x+")"
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


# Exceptions

class InvalidTransmutation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)