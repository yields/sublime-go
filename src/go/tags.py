
import go.buffer as buffer
import go.exec as exec
import go.log as log
import sublime

def add(view, edit, tag):
  """
  Add adds a tag name to view at point.
  """
  call(view, edit, [
    "--add-tags",
    tag,
  ])

def clear(view, edit):
  """
  Clear clears all tags.
  """
  call(view, edit, [
    "--clear-tags",
  ])

def call(view, edit, args):
  """
  Call gomodifytags(1) with args.

  The function will swap the current buffer
  on success and log out an error on failure.
  """
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
