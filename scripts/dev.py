
import sublime_plugin
import Golang.go

submodules = [
	'buffer',
	'commands',
	'conf',
	'coverage',
	'decorators',
	'errors',
	'escape',
	'exec',
	'gocode',
	'guru',
	'lint',
	'listeners',
	'log',
	'spinner',
	'tags',
	'test',
	'vet'
]

def plugin_loaded():
  for mod in submodules:
    sublime_plugin.reload_plugin('Golang.go.' + mod)
  Golang.go.log.DEBUG = '*'
  Golang.go.log.TRACE = True

