
from sublime import load_settings
from os import path

def vet_analyzers():
  settings = load_settings('Golang.sublime-settings')
  vet = settings.get('vet', {})
  return vet.get('analyzers', [])

def root():
  settings = load_settings("Golang.sublime-settings")
  return settings.get("root", "")

