import sublime
import sublime_plugin
from .components.meng import *

class ExampleCommand(sublime_plugin.TextCommand):

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

        extra = False
        error_status = False
        region_set = self.view.sel()

        if user_input[0] == "+":
            to_parse = user_input[1:]
            extra = True
        else:
            to_parse = user_input

        pipe_pattern = re.compile(r'''((?:[^|"'`]|"[^"]*"|'[^']*'|`[^`]*`)+)''')
        command_list = [x.strip() for x in pipe_pattern.split(to_parse)[1::2]]
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
            if extra:
                body = self.view.substr(region)+'\n\n'+body
            # call the transmutation to replace it on your screen
            if not error_status:
                # MAKE SURE YOU RE SET PROJECT DATA
                # project_data = sublime.active_window().project_data()
                # project_data['history'] = user_input
                # sublime.active_window().set_project_data(project_data)
                self.view.run_command("transmute", {"region_begin" : region.begin(), "region_end" : region.end(), "string" : body})


class TransmuteCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_begin, region_end, string):
        self.view.replace(edit, sublime.Region(region_begin, region_end), string)

