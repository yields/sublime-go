
from sublime import PhantomSet
from . import buffer

state = {}

def update(key, view, errors):
  phantoms = PhantomSet(view, key)
  dedupe = {}
  all = []

  for err in errors:
    if buffer.filename(view) == err.file:
      if err.line not in dedupe:
        all.append(err.to_phantom(view))
        dedupe[err.line] = True

  phantoms.update(all)
  state[id(key, view.id())] = phantoms

def remove(key, view):
  key = id(key, view.id())
  if key in state:
    state[key].update([])
    del state[key]

def remove_all():
  for key in state:
    state[key].update([])

def id(key, view_id):
  return key + ":" + str(view_id)
