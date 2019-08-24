
from tempfile import NamedTemporaryFile
from . import decorators
from . import buffer
from . import exec
from . import log
import sublime

@decorators.thread
@decorators.trace
def run(view):
  remove(view)

  pkg = buffer.package(view)
  file = buffer.filename(view)
  name = tmp()
  args = ['test', '--cover', '--coverprofile', name, '.']
  cmd = exec.Command('go', args=args, cwd=pkg)
  res = cmd.run()

  if res.code != 0:
    return

  mode = True
  report = []
  regions = []
  lines = 0

  with open(name) as f:
    for line in f.readlines():
      if not mode:
        item = parse(line)
        if item['count'] == 0:
          report.append(item)
      mode = False

  for item in report:
    if item['file'].endswith(file):
      for line in item['range']:
        point = view.text_point(line, 0)
        region = view.line(point)
        regions.append(region)
        lines += 1

  log.debug('cover: add {} regions {} uncovered lines', len(regions), lines)
  set_temporary_status(view, 'go ∙ {} uncovered lines'.format(lines))
  view.add_regions('go.coverage', regions, 'error', 'dot',
    sublime.HIDDEN
  )

def remove(view):
  view.erase_status('go.coverage')
  view.erase_regions('go.coverage')

def tmp():
  f = NamedTemporaryFile()
  f.close()
  return f.name

def parse(line):
  parts = line.split(':')
  file = parts[0]
  meta = parts[1].split(' ')
  ranges = meta[0].split(',')
  begin = int(ranges[0].split('.')[0])
  end = int(ranges[1].split('.')[0])
  return dict(
    file=file,
    range=[n for n in range(begin, end)],
    stmts=int(meta[1]),
    count=int(meta[2])
  )

def set_temporary_status(view, text):
  view.set_status('go.coverage', text)
  sublime.set_timeout(lambda: view.erase_status('go.coverage'), 5e3)
