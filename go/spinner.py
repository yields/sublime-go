
from sublime import set_timeout
from sublime import windows
import sublime
from threading import Lock
from . import log

def plugin_unloaded():
  log.debug('spinner: cleanup')
  for w in windows():
    for v in w.views():
      if v.id() in spinners:
        spinners[v.id()].reset()
        del spinners[v.id()]
        v.erase_status('golang')

spinners = {}

def lookup(view):
  id = view.id()
  if id not in spinners:
    spinners[id] = Spinner(view)
  return spinners[id]

def add(view, cmd):
  return lookup(view).add(cmd)

def remove(view, cmd):
  s = lookup(view).remove(cmd)
  if len(s.cmds) == 0:
    del spinners[view.id()]

def remove_all():
  for w in windows():
    for v in w.views():
      if v.id() in spinners:
        del spinners[v.id()]
        v.erase_status('golang')

class Spinner():
  def __init__(self, view):
    self.frames = ['⠁', '⠃', '⠇', '⠿', '⠸', '⠰', '⠠']
    self.cmds = set([])
    self.frame = 0
    self.view = view

  def add(self, cmd):
    self.cmds.add(cmd)
    if len(self.cmds) == 1:
      self.next()
    return self

  def next(self):
    if len(self.cmds) > 0:
      sublime.set_timeout(lambda: self.next(), 100)
      self.update()
    else:
      self.view.erase_status('go')

  def update(self):
    self.view.set_status('go', self.message())
    self.frame += 1

  def message(self):
    frame = self.frames[self.frame % len(self.frames)]
    cmd_text = ', '.join(self.cmds)
    msg = "{} Go ∙ {}\n".format(frame, cmd_text)
    return msg

  def remove(self, cmd):
    self.cmds.remove(cmd)
    return self

  def reset(self):
    self.cmds = set([])
