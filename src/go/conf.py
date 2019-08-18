
import os.path as path
import sublime

def vet_analyzers():
  settings = sublime.load_settings('go.sublime-settings')
  vet = settings.get('vet', {})
  return vet.get('analyzers', [])
