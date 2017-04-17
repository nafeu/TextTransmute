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

  An experimental sublime text plugin that allows you to mutate selected
  text in a style inspired by VIM, Emacs macros and shell programming tools.

  PRs, Questions, Issues -> @nafeu (github.com/nafeu)

  ----------------------------------------------------
  TO MAKE CUSTOM COMMANDS REFER TO:
  'Sublime Text 3/Packages/text-transmute/custom.py'
  ----------------------------------------------------

'''

import sublime
import sublime_plugin
import re
from .commands import *
from .custom import *
from .alias import *

PACKAGES_PATH = sublime.packages_path()
PLUGIN_PATH = PACKAGES_PATH + "/text-transmute"
PLATFORM = sublime.platform()
KEYMAP_PATH = '%s/Default (%s).sublime-keymap' % (PLUGIN_PATH, PLATFORM)
CUSTOM_COMMANDS_PATH = '%s/custom.py' % (PLUGIN_PATH)
ALIAS_PATH = '%s/alias.py' % (PLUGIN_PATH)

BUILT_IN_COMMANDS = [str(t).replace("<class 'text-transmute.commands.", "")
                     .replace("'>", "")
                     .lower()
                     for t in globals().values()
                     if ('text-transmute.commands.' in str(t)
                         and 'Test' not in str(t))]

CUSTOM_COMMANDS = [str(t).replace("<class 'text-transmute.custom.", "")
                   .replace("'>", "")
                   .lower()
                   for t in globals().values()
                   if ('text-transmute.custom.' in str(t)
                       and 'Test' not in str(t))]

AVAILABLE_COMMANDS = ["..."] + BUILT_IN_COMMANDS + CUSTOM_COMMANDS

# Sublime Text Plugin Commands

class TextTransmuteInitCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit):

        def on_done(text):
            self.view.run_command("text_transmute_parse",
                                  {"user_input": text})

        sublime.active_window().show_input_panel("Transmute Selection",
                                                 "",
                                                 on_done,
                                                 None,
                                                 None)


class TextTransmuteParseCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit, user_input):

        append_to_sel = False
        region_set = sublime.active_window().active_view().sel()

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

            body = sublime.active_window().active_view().substr(region)

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
                        error_logger.display_error("Transmutation Error: '" + str(e) + "'")
                        break
                else:
                    error_logger.display_error("Transmutation Error: '" + command + "' is not a valid command")
                    raise InvalidTransmutation(command)
                if append_to_sel:
                    body = sublime.active_window().active_view().substr(region)+'\n\n'+body

            sublime.active_window().active_view().run_command("text_transmute_exec", {"region_begin" : region.begin(),
                                                        "region_end" : region.end(),
                                                        "string" : body})

        reset_current_input()

class TextTransmuteExecCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)


class TextTransmuteListCommand(sublime_plugin.TextCommand):
    """
    TODO: Add docstring...
    """
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

            if selected_index == 0:
                sublime.active_window().show_input_panel("Transmute Selection",
                                                         current_input,
                                                         on_done,
                                                         on_change,
                                                         on_cancel)

            elif selected_index > 0:
                if len(current_input) > 1:
                    pipe = " | "
                updated_input = current_input + pipe + AVAILABLE_COMMANDS[selected_index]
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

    def run(self, edit):
        sublime.active_window().open_file(KEYMAP_PATH)

class TextTransmuteAddCustomCommands(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().open_file(CUSTOM_COMMANDS_PATH)

class TextTransmuteEditAlias(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().open_file(ALIAS_PATH)

class TextTransmuteAlias(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(selected_index):

            if (selected_index >= 0):
                self.view.run_command("text_transmute_parse",
                                      {"user_input": TRANSMUTATION_ALIASES[selected_index][1]})

        sublime.active_window().show_quick_panel(TRANSMUTATION_ALIASES, on_done)

# Helpers

def get_current_input():
    try:
        f = open(sublime.packages_path() + "/text-transmute/Data.sublime-project", 'r')
        return f.read()
    except FileNotFoundError:
        f = open(sublime.packages_path() + "/text-transmute/Data.sublime-project", 'w')
        f.write("")
        f.close()
        return ""

def set_current_input(text):
    f = open(sublime.packages_path() + "/text-transmute/Data.sublime-project", 'w')
    f.write(text)
    f.close()

def reset_current_input():
    f = open(sublime.packages_path() + "/text-transmute/Data.sublime-project", 'w')
    f.write("")
    f.close()


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
