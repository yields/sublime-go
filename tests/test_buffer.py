
from unittest.mock import (Mock, patch)
import go.buffer as buffer
import sublime

@patch("sublime.Region")
def test_replace(Region):
  view = Mock()
  edit = Mock()
  text = 'yo'

  view.viewport_position.return_value = 5
  view.size.return_value = 50
  buffer.replace(view, edit, text)

  reg = Region(0, 50)
  view.replace.assert_called_with(edit, reg, text)
  view.set_viewport_position.assert_called_with(5, False)

@patch("sublime.Region")
def test_text(Region):
  view = Mock()

  view.size.return_value = 50
  view.substr.return_value = 'text'

  text = buffer.text(view)

  assert text == b'text'
  view.substr.assert_called_with(Region(0, 50))

def test_is_go():
  view = Mock()

  view.match_selector.return_value = True
  result = buffer.is_go(view)

  assert result == True
  view.match_selector.assert_called_with(0, 'source.go')

def test_root():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = ['/myproject']

  root = buffer.root(view)

  assert root == '/myproject'

def test_root_no_folders():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = []
  view.file_name.return_value = '/tmp/main.go'

  root = buffer.root(view)

  assert root == '/tmp'

def test_filename():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = []
  view.file_name.return_value = '/tmp/main.go'

  file = buffer.filename(view)

  assert file == 'main.go'

def test_filename_has_root():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = ['/myproject']
  view.file_name.return_value = '/myproject/pkg/file.go'

  file = buffer.filename(view)

  assert file == 'pkg/file.go'

def test_package_has_no_root():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = []
  view.file_name.return_value = '/tmp/main.go'

  pkg = buffer.package(view)

  assert pkg == '/tmp/'

def test_package_has_root():
  view = Mock()
  window = Mock()

  view.window.return_value = window
  window.folders.return_value = ['/myproject']
  view.file_name.return_value = '/myproject/pkg/file.go'

  pkg = buffer.package(view)

  assert pkg == '/myproject/pkg'
