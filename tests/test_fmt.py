
from unittest.mock import (Mock, patch)
from go import fmt

@patch("sublime.Region")
def test_fmt(Region):
  region = Region()
  view = Mock()
  edit = Mock()
  win = Mock()

  view.viewport_position.return_value = 5
  view.substr.return_value = "package main; func main(){ fmt.Println(5 * 5) }"
  view.file_name.return_value = "/tmp/main.go"
  view.window.return_value = win
  win.folders.return_value = []

  fmt.run(view, edit)

  view.replace.assert_called_with(edit, region, 'package main\n\nimport "fmt"\n\nfunc main() { fmt.Println(5 * 5) }\n')
