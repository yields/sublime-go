
DEBUG = '-'
TRACE = False

def debug(msg, *args):
	if DEBUG == '*' or msg.startswith(DEBUG):
	  print("(go debug) " + msg.format(*args))

def error(msg, *args):
  print("(go errror) " + msg.format(*args))

