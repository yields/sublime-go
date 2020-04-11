
from . import decorators
from . import buffer
from . import exec
from . import log
import sublime
import json
import re

@decorators.trace
def complete(view, point):
  """
  Autocomplete the given view at point.
  """
  loc = "c" + str(point)
  root = buffer.root(view)
  file = buffer.filename(view)
  args = ["-f=json", "autocomplete", file, loc]
  stdin = buffer.text(view)
  cmd = exec.Command("gocode", args=args, stdin=stdin, cwd=root)
  res = cmd.run()

  if res.code != 0:
    log.error("gocode: {}", res.code, res.stderr)
    return

  res = json.loads(res.stdout)
  all = []

  if not res:
    return

  if len(res) == 0:
    return

  if res == None:
    return

  for item in enumerate(res[1]):
    all.append(parse(item[1]))

  log.debug("items: {}", all)

  return (all, sublime.INHIBIT_WORD_COMPLETIONS)

def parse(item):
  """
  Parses a gocode item and returns hint, subject.
  """
  log.debug('item {}', item)
  hint = item["class"][0].capitalize() + "・" + item["name"]
  subj = item["name"]

  if item["class"] == "func":
    func = parse_func(item)
    hint = "ƒ・{name}({args}) \t{rets}".format(**func)
    subj = func["snip"]

  return [hint, subj]

def parse_func(item):
  name = item.get('name')
  args, buf = parse_args(item['type'])
  rets = parse_returns(buf)
  preview_args = []
  named_args = []
  snip = ''

  for arg in args:
    prev = '{name} {type}'.format(**arg)
    preview_args.append(prev.strip())

  for i, arg in enumerate(args):
    placeholder = '{name} {type}'.format(**arg)
    placeholder = placeholder.replace('{', r'\{')
    placeholder = placeholder.replace('}', r'\}')
    tmpl = '${{{}:{}}}'.format(i + 1, placeholder.strip())
    named_args.append(tmpl)

  if len(named_args) > 0:
    snip = '{}({})'.format(name, ', '.join(named_args))
  else:
    snip = '{}()$0'.format(name)

  return {
    'name': name,
    'args': ', '.join(preview_args),
    'rets': '\t-> ({})'.format(', '.join(rets)),
    'snip': snip,
  }

def parse_args(buf, depth=0):
  """
  Parse args parses all function arguments.
  """
  buf = buf[len("func("):]
  arg = None
  all = []

  while len(buf) != 0:
    if buf[0] == ',':
      all.append(arg)
      arg = arg.copy()
      buf = buf[2:]
      continue

    if peek(buf, 'func('):
      args, buf = parse_args(buf, depth=depth+1)
      arg['type'] = 'func'
      arg['args'] = args
      continue

    if buf[0] == ')':
      if arg is not None:
        all.append(arg)
      buf = buf[1:]
      break

    if arg == None:
      arg = {'name': '', 'type': ''}

    (v,) = re.findall(r'^ *([!\.\w{}\[\]\/\*\>\< ]+)(?:[,)]|func\()', buf)
    buf = buf[len(v):]

    parts = v.split(' ')
    parts = [v.strip() for v in parts]

    if len(parts) == 2:
      arg['name'] = parts[0]
      arg['type'] = parts[1]
    else:
      arg['type'] = parts[0]

    # Not sure what this is from gocode(1), but clean it up.
    arg['type'] = cleanup(arg['type'])

  if depth > 0 and len(buf) > 0:
    n = buf.find(')')
    buf = buf[n:]

  if depth == 0:
    buf = buf.strip()

  return all, buf

def parse_returns(buf):
  if len(buf) > 0:
    if buf[0] == '(':
      buf = buf[1:-1]
    return [cleanup(v.strip()) for v in buf.split(',')]
  return []

def peek(buf, substr):
  return buf.startswith(substr)

def cleanup(v):
  if '!' in v:
    parts = v.split('!')
    return parts[0] + parts.pop()
  return v
