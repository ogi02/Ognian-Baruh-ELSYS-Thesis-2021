import json
import requests

# url related constants
HOST = "172.22.150.239"
PORT = "8080"
DEVICE_UID = "da:item:ZWave%2FFD72A41B%2F5:secure%2FC7E4BE6C8D78D27ECA253BF0DF3C5F7CCA187241%2F0x62%2FZWaveDoorLock"
LOCK_OPERATION = "setMode"

# door lock constants
OPERATION_LOCK = 255
OPERATION_UNLOCK = 0

# auth
USERNAME = "admin"
PASSWORD = "admin"

def lock_door():
	# set operation to lock
	mode = OPERATION_LOCK

	# generate headers
	headers = {"Accept": "application/json", "Content-Type": "application/json"}

	# generate url
	url = "http://" + host + ":" + port + "/m2m/fim/items/" + deviceuid + "/operations/" + operation

	# generate body
	data = json.dumps({"arguments": [mode]})

	# send request
	resp = requests.put(url, auth=(USERNAME, PASSWORD), headers=headers, data=data)

	print(resp.text)

def unlock_door():
	# set operation to lock
	mode = OPERATION_UNLOCK

	# generate headers
	headers = {"Accept": "application/json", "Content-Type": "application/json"}

	# generate url
	url = "http://" + host + ":" + port + "/m2m/fim/items/" + deviceuid + "/operations/" + operation

	# generate body
	data = json.dumps({"arguments": [mode]})

	# send request
	resp = requests.put(url, auth=(USERNAME, PASSWORD), headers=headers, data=data)

	print(resp.text)