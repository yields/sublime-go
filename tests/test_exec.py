
import go.exec as exec
import os.path as path

def test_goenv():
  orig = exec.environ
  exec.environ = { 'PATH': '/usr/local/bin' }
  v = exec.goenv('/')
  assert v.get('PATH') == ':'.join([
    '/usr/local/bin',
    path.join(v.get('GOPATH'), 'bin'),
  ])
  exec.environ = orig
