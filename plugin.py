'''
  _____  _____ __  __ _____
 |_   _|| ____|\ \/ /|_   _|
   | |  |  _|   \  /   | |
   | |  | |___  /  \   | |
   |_|  |_____|/_/\_\  |_|
  _____  ____      _     _   _  ____   __  __  _   _  _____  _____
 |_   _||  _ \    / \   | \ | |/ ___| |  \/  || | | ||_   _|| ____|
   | |  | |_) |  / _ \  |  \| |\___ \ | |\/| || | | |  | |  |  _|
   | |  |  _ <  / ___ \ | |\  | ___) || |  | || |_| |  | |  | |___
   |_|  |_| \_\/_/   \_\|_| \_||____/ |_|  |_| \___/   |_|  |_____|

  An experimental Sublime Text 3 plugin that allows you to mutate selected
  text in a style inspired by VIM, Emacs macros and shell programming tools.

  PRs, Questions, Issues -> @nafeu (github.com/nafeu)

  ----------------------------------------------------
  TO MAKE CUSTOM COMMANDS REFER TO:
  'Sublime Text 3/Packages/TextTransmute/custom.py'
  ----------------------------------------------------

'''

import sublime
import sublime_plugin
import re
import inspect
from .commands import *
from .custom import *
from .alias import *

HISTORY_LIMIT = 24
AVAILABLE_COMMANDS = [["...", "New Blank Transmutation"]] + \
                      [[t.__name__.lower(), inspect.getdoc(t)]
                      for t in globals().values()
                      if (('TextTransmute.commands' in str(t)
                      or 'TextTransmute.custom' in str(t))
                      and 'test' not in str(t).lower())]

# Sublime Text Plugin Commands

class TextTransmuteParseCommand(sublime_plugin.TextCommand):
    """ST3 plugin class for parsing user input before transmutation"""

    def run(self, edit, user_input):

        generate_data_files()

        success = True
        append_to_sel = False
        active_view = sublime.active_window().active_view()
        region_set = active_view.sel()
        err_log = WindowErrorLogger()
        ws_pattern = re.compile(r'''((?:[^\s"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')

        def strip_quotes(input_string):
            """Strip quotes from input string"""
            if ((input_string[0] == input_string[len(input_string)-1])
                    and (input_string[0] in ('"', "'"))):
                return input_string[1:-1]
            return input_string

        def eval_simple_expr(input_string):
            """Evaluate simple expression in input string"""
            if ((input_string[0] == input_string[len(input_string)-1])
                    and (input_string[0] in '`')):
                return eval_expr(input_string[1:-1])
            return input_string

        def clean_param(param):
            """Strip quotes and evaluate any embedded expressions in param"""
            return str(eval_simple_expr(strip_quotes(param)))

        if user_input[0] == "+":
            to_parse = user_input[1:]
            append_to_sel = True
        else:
            to_parse = user_input

        command_list = [c.strip() for c in pipe_pattern.split(to_parse)[1::2]]

        for region in region_set:

            body = active_view.substr(region)

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
                        t = globals()[command_name.capitalize()](err_log)
                        body = str(t.transmute(body, params))
                    except Exception as e:
                        success = False
                        err_log.display_err("Transmute Error: '%s'" % (str(e)))
                        break
                else:
                    success = False
                    err_log.display_err("%s: '%s' %s" % ("Transmute Error",
                                                         command,
                                                         "is not a command."))
                    raise InvalidTransmutation(command)
                if append_to_sel:
                    body = active_view.substr(region)+'\n\n'+body

            transmutation_inputs = {"region_begin" : region.begin(),
                                    "region_end" : region.end(),
                                    "string" : body}

            active_view.run_command("text_transmute_exec",
                                    transmutation_inputs)

        if success:
            append_to_history(user_input)
            reset_current_input()

class TextTransmuteExecCommand(sublime_plugin.TextCommand):
    """ST3 plugin class for replacing selected area with its mutation"""

    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit,
                          sublime.Region(region_begin, region_end),
                          string)


class TextTransmuteInitCommand(sublime_plugin.TextCommand):
    """ST3 plugin class for replacing selected area with its mutation"""

    def run(self, edit):

        def on_done(text):
            self.view.run_command("text_transmute_parse", {"user_input": text})
            reset_current_input()

        def on_change(text):
            set_current_input(text)

        def on_cancel():
            reset_current_input()

        def on_select(selected_index):

            current_input = get_current_input()
            pipe = ""
            ws = " "

            if selected_index == 0:
                sublime.active_window().show_input_panel("Transmute Selection",
                                                         current_input + ws,
                                                         on_done,
                                                         on_change,
                                                         on_cancel)

            elif selected_index > 0:
                if len(current_input) > 1:
                    pipe = " | "
                updated_input = (current_input +
                                 pipe +
                                 AVAILABLE_COMMANDS[selected_index][0] +
                                 ws)
                sublime.active_window().show_input_panel("Transmute Selection",
                                                         updated_input,
                                                         on_done,
                                                         on_change,
                                                         on_cancel)
                set_current_input(updated_input)

            else:
                pass

        sublime.active_window().show_quick_panel(AVAILABLE_COMMANDS, on_select)


class TextTransmuteEditKeyBinds(sublime_plugin.TextCommand):
    """ST3 plugin class for editing key binds"""

    def run(self, edit):
        formatted_platform = format_platform(sublime.platform())
        keymap_path = '%s/%s/Default (%s)%s' % (sublime.packages_path(),
                                                "TextTransmute",
                                                formatted_platform,
                                                ".sublime-keymap")
        sublime.active_window().open_file(keymap_path)


class TextTransmuteAddCustomCommands(sublime_plugin.TextCommand):
    """ST3 plugin class for adding custom commands"""

    def run(self, edit):
        custom_commands_path = '%s/%s/%s' % (sublime.packages_path(),
                                             "TextTransmute",
                                             "custom.py")
        sublime.active_window().open_file(custom_commands_path)


class TextTransmuteEditAlias(sublime_plugin.TextCommand):
    """ST3 plugin class for adding and editing aliases"""

    def run(self, edit):
        alias_path = '%s/%s/%s' % (sublime.packages_path(),
                                   "TextTransmute",
                                   "alias.py")
        sublime.active_window().open_file(alias_path)


class TextTransmuteAlias(sublime_plugin.TextCommand):
    """ST3 plugin class for using aliased transmutation scripts"""

    def run(self, edit):

        def on_done(selected_index):

            if (selected_index >= 0):
                self.view.run_command("text_transmute_parse",
                                      {"user_input": ALIASES[selected_index][1]})

        sublime.active_window().show_quick_panel(ALIASES, on_done)


class TextTransmuteHistory(sublime_plugin.TextCommand):
    """ST3 plugin class for accessing command usage history"""

    def run(self, edit):

        history = get_history()

        def on_done(text):
            self.view.run_command("text_transmute_parse", {"user_input": text})

        def on_change(text):
            set_current_input(text)

        def on_cancel():
            reset_current_input()

        def on_select(selected_index):
            sublime.active_window().show_input_panel("Transmute Selection",
                                                   history[selected_index],
                                                   on_done,
                                                   on_change,
                                                   on_cancel)

        sublime.active_window().show_quick_panel(history, on_select)


# Helpers

def get_current_input():
    """Get current input value from Data.sublime-project"""

    try:
        f = open('%s/%s/%s' % (sublime.packages_path(),
                               "TextTransmute",
                               "Data.sublime-project"), 'r')
        return f.read()
    except FileNotFoundError:
        f = open('%s/%s/%s' % (sublime.packages_path(),
                               "TextTransmute",
                               "Data.sublime-project"), 'w')
        f.write("")
        f.close()
        return ""


def set_current_input(text):
    """Set current input value in Data.sublime-project"""

    f = open('%s/%s/%s' % (sublime.packages_path(),
                           "TextTransmute",
                           "Data.sublime-project"), 'w')
    f.write(text)
    f.close()


def reset_current_input():
    """Reset current input value in Data.sublime-project"""

    file_name = '%s/%s/%s' % (sublime.packages_path(),
                              "TextTransmute",
                              "Data.sublime-project")
    with open(file_name, "w"):
        pass


def get_history():
    """Get command usage history from History.sublime-project"""

    f = open('%s/%s/%s' % (sublime.packages_path(),
                           "TextTransmute",
                           "History.sublime-project"), 'r')
    content = f.readlines()
    f.close()
    return [x.strip() for x in content]


def append_to_history(text):
    """Append to command usage history in History.sublime-project"""

    file_name = '%s/%s/%s' % (sublime.packages_path(),
                              "TextTransmute",
                              "History.sublime-project")
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(file_name, 'w') as fout:
        if len(data) > HISTORY_LIMIT:
            fout.writelines(data[1:] + ["\n" + text])
        elif len(data) < 1:
            fout.writelines([text])
        else:
            fout.writelines(data + ["\n" + text])


def reset_history():
    """Reset command usage history in History.sublime-project"""

    f = open('%s/%s/%s' % (sublime.packages_path(),
                           "TextTransmute",
                           "History.sublime-project"), 'w')
    f.write("")
    f.close()


def format_platform(platform):
    """Return formatted uppercase or capitalized platform value"""

    if platform == "linux" or platform == "windows":
        return platform.capitalize()
    else:
        return platform.upper()


def generate_data_files():
    """Generate data files for use by plugin"""

    data_file_name = '%s/%s/%s' % (sublime.packages_path(),
                                   "TextTransmute",
                                   "Data.sublime-project")
    hist_file_name = '%s/%s/%s' % (sublime.packages_path(),
                                   "TextTransmute",
                                   "History.sublime-project")
    try:
        file = open(data_file_name, 'r')
    except FileNotFoundError:
        file = open(data_file_name, 'w')
    try:
        file = open(hist_file_name, 'r')
    except FileNotFoundError:
        file = open(hist_file_name, 'w')


# Exception Handling

class WindowErrorLogger(object):
    """Display error message in sublime window"""

    def display_err(self, message):
        sublime.error_message(message)


class InvalidTransmutation(Exception):
    """Exception describing invalid transmutation"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
