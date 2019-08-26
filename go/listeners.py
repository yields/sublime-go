
from . import coverage
from . import errors
from . import buffer
from . import gocode
from . import guru
from . import log
import sublime_plugin
import sublime
import time

class Listener(sublime_plugin.ViewEventListener):
  def __init__(self, view):
    self.view = view

  def on_pre_save(self):
    if not self.view.is_dirty():
      self.view.run_command('go_fmt')

  def on_post_save_async(self):
    self.view.run_command('go_vet')
    self.view.run_command('go_lint')

  def on_modified_async(self):
    errors.remove_all()
    coverage.remove(self.view)

  def on_query_completions(self, prefix, points):
    if buffer.is_go(self.view):
      return gocode.complete(self.view, points[0])

  @staticmethod
  def applies_to_primary_view_only():
    return True
