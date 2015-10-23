import sublime, sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
  def on_done(self, index):
    self.view.run_command("insert_my_text", {"args":{'text':self.list[index]}})

  def run(self, edit):
    self.list = ["one", "two", "buckle my", "shoe"]
    self.view.window().show_quick_panel(self.list, self.on_done)

class InsertMyText(sublime_plugin.TextCommand):
  def run(self, edit, args):
    self.view.insert(edit, 0, args['text'])

