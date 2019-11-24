
from os import path
from . import decorators
from . import buffer
from . import errors
from . import lint
from . import exec

@decorators.trace
def run(view, edit):
  """
  Run runs goimports(1) on the given view.
  """
  errors.remove("fmt", view)
  file = buffer.filename(view)
  pos = view.viewport_position()
  src = buffer.text(view)
  args = ["-e", "-srcdir", path.dirname(file)]
  root = buffer.root(view)
  pkg = buffer.package(view)
  cmd = exec.Command("goimports", args=args, stdin=src, cwd=pkg)
  res = cmd.run()

  if res.code == 0:
    buffer.replace(view, edit, res.stdout)
    return

  errs = lint.parse(res.stderr, (root, pkg, file), "fmt")
  errors.update("fmt", view, errs)
