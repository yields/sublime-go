
from sublime_plugin import reload_plugin
from .go import listeners
from .go import commands

submodules = [
  'buffer',
  'commands',
  'conf',
  'decorators',
  'errors',
  'escape',
  'exec',
  'fmt',
  'gocode',
  'guru',
  'lint',
  'listeners',
  'log',
  'spinner',
  'tags',
  'test',
  'vet',
]

def plugin_loaded():
  for mod in submodules:
    reload_plugin('Golang.go.' + mod)
