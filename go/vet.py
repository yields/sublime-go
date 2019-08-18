
from . import decorators
from . import buffer
from . import errors
from . import conf
from . import lint
from . import exec
from . import log
import os.path as path
import sublime
import sys

@decorators.thread
@decorators.trace
def run(view, edit):
  """
  Run runs go vet(1) on the given view.
  """
  errors.remove("vet", view)
  root = buffer.root(view)
  file = buffer.filename(view)
  pkg = buffer.package(view)

  # When sublime is opened with `$ subl main.go`
  if len(view.window().folders()) == 0:
    pkg = file

  args = ["vet"] + ["--" + a for a in conf.vet_analyzers()] + [pkg]
  cmd = exec.Command("go", args=args, cwd=root)
  res = cmd.run()

  if res.code != 0:
    errs = lint.parse(res.stderr, file, "vet")
    log.debug('vet: {}', errs)
    errors.update("vet", view, errs)
