
import sublime

def vet_analyzers():
  settings = sublime.load_settings('golang.sublime-settings')
  vet = settings.get('vet', {})
  return vet.get('analyzers', [])
