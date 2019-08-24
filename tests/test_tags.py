
import go.tags as tags

def test_parse_empty_text():
  (key, case) = tags.parse('')
  assert key == 'json'
  assert case == 'snakecase'

def test_parse_key():
  (key, case) = tags.parse('xml')
  assert key == 'xml'
  assert case == 'snakecase'

def test_parse_key_case():
  (key, case) = tags.parse('xml lispcase')
  assert key == 'xml'
  assert case == 'lispcase'
