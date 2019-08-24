
import sublime_plugin
import Golang.go

submodules = [v for v in dir(Golang.go) if not v.startswith('__')]

def plugin_loaded():
  for mod in submodules:
    sublime_plugin.reload_plugin('Golang.go.' + mod)
  Golang.go.log.DEBUG = '*'
  Golang.go.log.TRACE = True

