
import os.path as path
import sublime

def replace(view, edit, text):
  """
  Replace the whole buffer in view.
  """
  pos = view.viewport_position()
  region = sublime.Region(0, view.size())
  view.replace(edit, region, text)
  view.set_viewport_position(pos, False)


def text(view):
  """
  Text returns all text from the view.
  """
  reg = sublime.Region(0, view.size())
  return view.substr(reg).encode('UTF-8')

def is_string(view, point):
  """
  Is string returns true if point is within a string.
  """
  return view.match_selector(point, 'string')

def is_comment(view, point):
  """
  Is comment returns true if point is within a comment.
  """
  return view.match_selector(point, "comment")

def can_complete(view, point):
  """
  Can complete returns true if it's possible complete point.
  """
  if not is_go(view):
    return False

  if is_string(view, point):
    return False

  if is_comment(view, point):
    return False

  (row, _) = view.rowcol(point)
  return row > 0

def in_struct(view):
  """
  In struct retrieves the current cursor
  position and checks to see if we are
  inside a struct.
  """
  scopes = ['source.go', 'meta.type.go']
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
