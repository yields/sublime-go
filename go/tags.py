
from . import buffer
from . import exec
from . import log
import sublime

cases = {
  'snakecase': 'snake_case',
  'camelcase': 'camelCase',
  'lispcase': 'lisp-case',
  'pascalcase': 'PascalCase',
  'keep': 'keep',
}

def add(view, edit, tag):
  (key, case) = parse(tag)
  call(view, edit, [
    "--add-tags",
    key,
    '--transform',
    case
  ])

def clear(view, edit):
  call(view, edit, [
    "--clear-tags",
  ])

def call(view, edit, args):
  off = view.sel()[0].begin()
  file = view.file_name()
  args += ["--offset", str(off)]
  args += ["--file", file]
  cmd = exec.Command("gomodifytags", args=args)
  res = cmd.run()

  if res.code == 0:
    reg = sublime.Region(0, view.size())
    view.replace(edit, reg, res.stdout)
    return

  log.error("gomodifytags(1) - {} {}", res.code, res.stderr)

def parse(text):
  if len(text) == 0:
    return ('json', 'snakecase')
  parts = text.split(' ')
  if len(parts) == 1:
    return (parts[0], 'snakecase')
  return (parts[0], parts[1])
