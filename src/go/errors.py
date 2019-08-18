
import go.buffer as buffer
import sublime

state = {}

def update(key, view, errors):
  """
  Update updates the set of shown errors.

  The method shos a given list of errors on the given
  view, keyed by `key`, each tool uses a different key.
  """
  set = sublime.PhantomSet(view, key)
  all = []

  for err in errors:
    if buffer.filename(view) == err.file:
        all.append(err.to_phantom(view))

  set.update(all)
  state[id(key, view.id())] = set


def remove(key, view):
  """
  Remove removes all errors from view of key.
  """
  key = id(key, view.id())
  if key in state:
    state[key].update([])
    del state[key]

def remove_all():
  for key in state:
    state[key].update([])

def id(key, view_id):
  return key + ":" + str(view_id)
