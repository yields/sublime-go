
import go.decorators as decorators
import go.buffer as buffer
import go.exec as exec
import go.log as log
import sublime
import json

@decorators.thread
@decorators.trace
def run(view):
  """
  Run runs the tests and returns a new test Report.
  """
  pkg = buffer.package(view)
  cmd = exec.Command("go", args=["test", "-json", "."], cwd=pkg)
  res = cmd.run()

  if res.code == 2:
    log.debug('test: unexpected error {}', res.stderr)
    return Report()

  ret = Report()
  for line in res.stdout.splitlines():
    ret.add(json.loads(line))

  return ret

class Report():
  def __init__(self):
    self.items = []

  def add(self, item):
    item = { k.lower(): v for k, v in item.items() }
    self.items.append(item)

  def text(self):
    last = self.items[len(self.items)-1]
    return "{action} {elapsed}s".format(**last)
