
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
  Run runs staticcheck(1) on the given view.
  """
  errors.remove("staticcheck", view)
  root = buffer.root(view)
  file = buffer.filename(view)
  pkg = buffer.package(view)
  checks = conf.static_checks()

  if len(checks) == 0:
    log.debug('staticcheck: no checks to run')
    return

  all = ','.join(checks)
  args = ['--checks', all, pkg]
  cmd = exec.Command("staticcheck", args=args, cwd=root)
  res = cmd.run()

  if res.code != 0:
    errs = lint.parse(res.stdout, (root, root, file), "staticcheck")
    log.debug('staticcheck: {}', errs)
    errors.update("staticcheck", view, errs)
