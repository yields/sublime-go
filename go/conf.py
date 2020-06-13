
from sublime import load_settings
from os import path

def vet_analyzers():
  settings = load_settings('Golang.sublime-settings')
  vet = settings.get('vet', {})
  return vet.get('analyzers', [])

def static_checks():
  settings = load_settings('Golang.sublime-settings')
  sc = settings.get('staticcheck', {})
  return sc.get('checks', [])

def root():
  settings = load_settings("Golang.sublime-settings")
  return settings.get("root", "")

def vet_on_post_save():
  settings = load_settings('Golang.sublime-settings')
  vet = settings.get('vet', {})
  return vet.get('run_on_post_save', True)
