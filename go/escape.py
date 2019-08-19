
from . import decorators
from . import buffer
from . import errors
from . import lint
from . import exec

@decorators.thread
@decorators.trace
def run(view, edit):
  """
  Run runs go build(1) with --gcflags -m to show escape analysis.
  """
  errors.remove("escape", view)

  args = ['build', '--gcflags=-m', '.']
  pkg = buffer.package(view)
  cmd = exec.Command("go", args=args, cwd=pkg)
  res = cmd.run()

  if res.code == 0:
    file = buffer.filename(view)
    errs = lint.parse(res.stderr, file, "escape")
    errs = filter(errs, file, "escapes to heap")
    errors.update("escape", view, errs)

def filter(errors, file, msg):
  ret = []
  for err in errors:
    if file == err.file and msg in err.msg:
      ret.append(err)
  return ret
