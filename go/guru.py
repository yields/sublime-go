
from . import decorators
from . import exec
from . import log
import os.path as path
import sublime
import time
import json

@decorators.thread
@decorators.trace
def source(view):
  locate(view)

def call(mode, filename, region):
  """
  Call calls guru(1) with the given `<mode>`
  filename and point.
  """
  file = "{}:#{},#{}".format(filename, region.begin(), region.end())
  args = ["--json", mode, file]
  cmd = exec.Command("guru", args=args)
  res = cmd.run()
  if res.code == 0:
    return json.loads(res.stdout)

def locate(view):
  """
  Locate returns the location of the symbol
  at the cursor, empty string is returned if no symbol
  is found.
  """
  file = view.file_name()
  pos = view.sel()[0]
  resp = call("describe", file, pos)

  if resp == None:
    return

  if resp["detail"] == "value":
    if 'objpos' in resp['value']:
      open_position(view, resp['value']['objpos'])
      return

  if resp["detail"] == "type":
    if "namepos" in resp["type"]:
      open_position(view, resp['type']['namepos'])
      return

  if 'built-in type' in resp['desc']:
    symbol = resp['type']['type']
    cwd = path.dirname(file)
    goroot = exec.goenv(cwd)['GOROOT']
    src = path.join(goroot, 'src', 'builtin', 'builtin.go')
    win = view.window()
    open_symbol(view, src, symbol)
    return

  log.error("guru(1) - unknown response {}", resp)
  return ""

def open_position(view, src):
  win = view.window()
  win.open_file(src, sublime.ENCODED_POSITION)

def open_symbol(view, src, symbol):
  win = view.window()
  new_view = win.open_file(src)
  show(new_view, symbol)
  sublime.set_timeout(lambda: show(new_view, symbol), 20)

def show(view, symbol):
  if view.is_loading():
    sublime.set_timeout(lambda: show(view, symbol), 30)
    return
  for sym in view.symbols():
    if symbol in sym[1]:
      sel = sublime.Selection(0)
      sel.add(sym[0])
      view.show(sel)


