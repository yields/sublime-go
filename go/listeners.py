
from . import coverage
from . import errors
from . import buffer
from . import gocode
from . import conf
from . import guru
from . import log
import sublime_plugin
import sublime
import time

class Listener(sublime_plugin.ViewEventListener):
  def __init__(self, view):
    self.view = view

  def on_pre_save(self):
    if self.view.is_dirty():
      self.view.run_command('go_fmt')

  def on_post_save_async(self):
    if conf.vet_on_post_save():
      self.view.run_command('go_vet')

    self.view.run_command('go_lint')
    self.view.run_command('go_static_check')

  def on_modified_async(self):
    errors.remove_all()
    coverage.remove(self.view)

  def on_query_completions(self, prefix, points):
    if not buffer.can_complete(self.view, points[0]):
      return

    log.debug('complete prefix={} points={}', prefix, points)

    if sublime.version() < '4070':
      return gocode.complete(self.view, points[0])

    req = Request(self.view, points)
    req.send_async()
    return req.completions

  @staticmethod
  def applies_to_primary_view_only():
    return True

class Request():
  def __init__(self, view, points):
    self.view = view
    self.points = points
    self.completions = sublime.CompletionList()

  def send_async(self):
    sublime.set_timeout_async(self.send, 0)

  def send(self):
    all = gocode.complete(self.view, self.points[0])

    if all is None:
      return

    self.completions.set_completions(all[0], all[1])
