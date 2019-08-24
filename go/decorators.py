
import sublime
import time
from . import log

def trace(func):
  def tracer(*args, **kwargs):
    start = now()
    name = nameof(func)
    if log.TRACE:
      print('(go trace) {}'.format(name))
    resp = func(*args, **kwargs)
    if log.TRACE:
      print('(go trace) {} ({}ms)'.format(
        name,
        now() - start
      ))
    return resp
  return tracer

def now():
  return int(round(time.time() * 1e3))

def nameof(func):
  return '{}.{}'.format(
    func.__module__[len('golang.'):],
    func.__name__,
  )

def memoized(func):
  mem = {}
  def call(*args, **kwargs):
    if args not in mem:
      mem[args] = func(*args, **kwargs)
    return mem[args]
  return call

def thread(func):
  def run(*args, **kwargs):
    return Promise(func, args, kwargs)
  return run

class Promise():
  def __init__(self, func, args, kwargs):
    self.func = func
    self.args = args
    self.kwargs = kwargs

  def then(self, cb):
    sublime.set_timeout_async(lambda:
      self.call(cb, *self.args, **self.kwargs),
      0)

  def call(self, cb, *args, **kwargs):
    v = None
    try:
      v = self.func(*args, **kwargs)
    finally:
      cb(v)
