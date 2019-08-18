
import go.decorators as decorators
import go.buffer as buffer
import go.errors as errors
import go.lint as lint
import go.exec as exec
import os.path as path

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
  pkg = buffer.package(view)
  cmd = exec.Command("goimports", args=args, stdin=src, cwd=pkg)
  res = cmd.run()

  if res.code == 0:
    buffer.replace(view, edit, res.stdout)
    return

  errs = lint.parse(res.stderr, file, "fmt")
  errors.update("fmt", view, errs)
