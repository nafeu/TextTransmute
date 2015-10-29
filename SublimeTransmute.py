import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(text):
            # self.view.run_command("insert", {"characters": text})
            if (text == 'length'):
                # print("length works")
                for region in self.view.sel():
                    length = str(len(self.view.substr(region)))
                    region_begin = region.begin()
                    region_end = region.end()
                    # self.view.run_command("replace", {"region": region, "string": "asdf", "asdf": "asdf"})
                    # self.view.run_command("insert", {"characters": length})
                    self.view.run_command("transmute", {"region_begin": region_begin, "region_end": region_end, "string": length})
            else:
                sublime.error_message("invalid command")

        sublime.active_window().show_input_panel("caption", "length", on_done, None, None)

        # self.view.replace(edit, self.view.size(), output)

class ParseCommand(sublime_plugin.TextCommand):
    def run(self, edit, user_input):
        command_list = user_input.split("|")


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

