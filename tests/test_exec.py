
import go.exec as exec
import os.path as path
import os

def test_goenv():
  orig = exec.environ
  exec.environ = { 'PATH': '/usr/local/bin' }
  pkg = path.join(os.getcwd(), 'examples')
  v = exec.goenv(pkg, timeout=10)
  assert v.get('PATH') == ':'.join([
    '/usr/local/bin',
    path.join(v.get('GOPATH'), 'bin'),
  ])
  exec.environ = orig
