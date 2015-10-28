import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(text):
            self.view.run_command("insert", {"characters": text})

        selection = self.view.sel()
        output = ''

        for region in self.view.sel():
            length = str(len(self.view.substr(region)))
            self.view.replace(edit, region, length)
            # output += '\n' + self.view.substr(region)

        # self.view.replace(edit, self.view.size(), output)

        # sublime.active_window().show_input_panel("caption", "initial_text", on_done, None, None)

