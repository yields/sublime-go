
from . import decorators
from . import buffer
from . import errors
from . import exec
from . import log
import os.path as path
import string
import sublime
import html
import sys

@decorators.thread
@decorators.trace
def run(view, edit):
  """
  Run runs golint(1) on the given view.
  """
  errors.remove("lint", view)
  file = buffer.filename(view)
  root = buffer.root(view)
  cmd = exec.Command("golint", args=[file], cwd=root)
  res = cmd.run()

  if res.code == 0:
    errs = parse(res.stdout, file, "lint")
    errors.update("lint", view, errs)


def parse(str, file, tool):
  """
  Parse parses the given str matching any
  lint errors and returns a list of errors
  that match the given str.

  If one of the lines is not parseable, it is
  logged and ignored.
  """
  errs = []
  for l in str.splitlines():
    err = Error.parse(l, file, tool)
    if err is not None:
      errs.append(err)
  return errs

template = string.Template(r"""
  <body id="go-error">
    <style>
      div.error {
        background-color: color(var(--background) blend(orange 99%));
        border-left: 0.2rem solid color(var(--foreground) blend(orange 60%));
        margin-left: 0.5rem;
        color: color(var(--foreground) blend(orange 99%));
        padding: 0 1rem;
        position: relative;
        margin-top: 1px;
      }
    </style>
    <div class="error">$tool: $msg</div>
  </body>
""")

class Error():
  """
  Error represents a linter error at a specific
  line, column with a given msg.
  """
  def __init__(self, file, tool, line, col, msg):
    self.file = file.strip()
    self.tool = tool
    self.line = line
    self.col = col
    self.msg = msg

  def to_phantom(self, view):
    point = view.text_point(self.line-1, 0)
    region = view.line(point)
    pos = region.end()
    html = template.substitute(**self.args())
    return sublime.Phantom(
      sublime.Region(pos, pos),
      html,
      sublime.LAYOUT_INLINE
    )

  def args(self):
    """
    minihtml does not support some entities like " and '.
    """
    msg = html.escape(self.msg)
    msg = msg.replace('&quot;', '"')
    msg = msg.replace('&#x27', "'")
    return {
      'tool': self.tool,
      'msg': msg,
    }

  def __str__(self):
    return ':'.join([
      self.tool,
      self.file,
      str(self.line),
      str(self.col),
    ]) + " " + self.msg

  def __repr__(self):
    return self.__str__()

  @staticmethod
  def parse(line, filename, tool):
    """
    Parse the given line and return an error.

    If an invalid line is given, None is returned.
    """

    if line.startswith('vet:'):
      line = line[len('vet:'):]

    if line.find(':') != -1:
      parts = line.split(':', 3)
      file = parts[0].strip()
      parts = [s.strip() for s in parts[1:]]

      if line.find('<standard input>') != -1:
        file = filename
      elif file.startswith('./'):
        file = file[2:]

      if not parts[1].isdigit():
        row = int(parts[0])
        msg = parts[1]
        return Error(file, tool, row, 0, msg)

      row = int(parts[0])
      col = int(parts[1])
      msg = parts[2]

      return Error(file, tool, row, col, msg)
