import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        def on_done(text):
            print(text);
            self.view.run_command("insert", {"characters": text})
        # self.view.insert(edit, self.view.size(), 'Hello, world!')
        sublime.active_window().show_input_panel("caption", "initial_text", on_done, None, None)
