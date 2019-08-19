
from sublime import Region
from os import path

def replace(view, edit, text):
  """
  Replace the whole buffer in view.
  """
  pos = view.viewport_position()
  region = Region(0, view.size())
  view.replace(edit, region, text)
  view.set_viewport_position(pos, False)


def text(view):
  """
  Text returns all text from the view.
  """
  reg = Region(0, view.size())
  return view.substr(reg).encode('utf-8')


def in_struct(view):
  """
  In struct retrieves the current cursor
  position and checks to see if we are
  inside a struct.
  """
  scopes = ['source.go', 'variable.other.member.declaration.go']
  point = view.sel()[0].b
  return view.match_selector(point, " ".join(scopes))


def is_go(view):
  """
  Is golang returns true if the given view
  is a golang file.
  """
  return view.match_selector(0, "source.go")

def root(view):
  """
  root returns the root from the given view
  """
  all = view.window().folders()
  if len(all) == 1:
    return all[0]
  return path.dirname(view.file_name())

def filename(view):
  """
  Filename returns a relative filename from view.
  """
  return view.file_name()[len(root(view))+1:]

def package(view):
  """
  Package returns the path to pkg that contains view.
  """
  file = filename(view)
  pkg = path.dirname(file)
  return path.join(root(view), pkg)
