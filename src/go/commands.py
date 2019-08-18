
import go.spinner as spinner
import go.buffer as buffer
import go.escape as escape
import go.test as test
import go.tags as tags
import go.guru as guru
import go.lint as lint
import go.log as log
import go.fmt as fmt
import go.vet as vet
import sublime_plugin
import sublime

class GoFmtCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    fmt.run(self.view, edit)

  def is_enabled(self):
    return buffer.is_go(self.view)

class GoVetCommand(sublime_plugin.TextCommand):
  locked = False

  def run(self, edit):
    if not self.locked:
      self.lock()
      p = vet.run(self.view, edit)
      p.then(lambda _: self.unlock())

  def lock(self):
    self.locked = True
    spinner.add(self.view, 'vet')

  def unlock(self):
    self.locked = False
    spinner.remove(self.view, 'vet')

  def is_enabled(self):
    return buffer.is_go(self.view)

class GoLintCommand(sublime_plugin.TextCommand):
  locked = False

  def run(self, edit):
    if not self.locked:
      self.lock()
      p = lint.run(self.view, edit)
      p.then(lambda _: self.unlock())

  def lock(self):
    self.locked = True
    spinner.add(self.view, 'lint')

  def unlock(self):
    self.locked = False
    spinner.remove(self.view, 'lint')

  def is_enabled(self):
    return buffer.is_go(self.view)

class GoEscapeCommand(sublime_plugin.TextCommand):
  locked = False

  def run(self, edit):
    if not self.locked:
      self.lock()
      p = escape.run(self.view, edit)
      p.then(lambda _: self.unlock())

  def lock(self):
    self.locked = True
    spinner.add(self.view, 'escape')

  def unlock(self):
    self.locked = False
    spinner.remove(self.view, 'escape')

  def is_enabled(self):
    return buffer.is_go(self.view)

class GoSourceCommand(sublime_plugin.TextCommand):
  locked = False

  def run(self, edit):
    if not self.locked:
      self.lock()
      p = guru.source(self.view)
      p.then(lambda _: self.unlock())

  def lock(self):
    self.locked = True
    spinner.add(self.view, 'source')

  def unlock(self):
    self.locked = False
    spinner.remove(self.view, 'source')

  def is_enabled(self, event=None):
    return buffer.is_go(self.view)

class GoTestCommand(sublime_plugin.TextCommand):
  locked = False

  def run(self, edit):
    if not self.locked:
      self.lock()
      p = test.run(self.view)
      p.then(lambda msg: self.unlock(msg))

  def lock(self):
    self.locked = True
    spinner.add(self.view, 'test')

  def unlock(self, report):
    self.locked = False
    spinner.remove(self.view, 'test')
    self.set_report(report)

  def set_report(self, report):
    msg = 'go ∙ ' + report.text()
    key = 'go.test'
    self.view.set_status(key, msg)
    sublime.set_timeout(lambda: self.view.erase_status(key), 10e3)

  def is_enabled(self, event=None):
    return buffer.is_go(self.view)

class GoAddTagsCommand(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    tag = args["tag_name_input"]
    tags.add(self.view, edit, tag)

  def is_enabled(self):
    return buffer.in_struct(self.view)

  def description(self):
    return "add tags to a struct"

  def input(self, args):
    return TagNameInput()

class GoSetTagsCommand(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    tag = args["tag_name_input"]
    tags.set(self.view, edit, tag)

  def is_enabled(self):
    return buffer.in_struct(self.view)

  def description(self):
    return "set tags on a struct"

  def input(self, args):
    return TagNameInput()

class GoClearTagsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    tags.clear(self.view, edit)

  def is_enabled(self):
    return buffer.in_struct(self.view)

  def description(self):
    return "clear tags on a struct"

class TagNameInput(sublime_plugin.TextInputHandler):
  def placeholder(self):
    return "json"
  def validate(self, text):
    return True


class ViewLock():
  def __enter__(self):
    print("enter")

  def __exit__(self, *args):
    print("exit {}", args)
