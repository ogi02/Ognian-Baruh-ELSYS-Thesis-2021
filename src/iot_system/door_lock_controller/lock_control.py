# library imports
import json
import requests

# project imports
from constants import *

# url related constants
PORT = "8080"
DEVICE_UID = "da:item:ZWave%2FFD72A41B%2F5:secure%2FC7E4BE6C8D78D27ECA253BF0DF3C5F7CCA187241%2F0x62%2FZWaveDoorLock"
LOCK_OPERATION = "setMode"

# door lock constants
OPERATION_LOCK = 255
OPERATION_UNLOCK = 0

# auth
USERNAME = "admin"
PASSWORD = "admin"


def lock_door() -> None:
	# set operation to lock
	operation = OPERATION_LOCK

	# invoke operation
	print(invoke_operation(operation))


def unlock_door() -> None:
	# set operation to lock
	operation = OPERATION_UNLOCK

	# invoke operation
	print(invoke_operation(operation))


def invoke_operation(operation: int) -> str:
	# generate headers
	headers = {"Accept": "application/json", "Content-Type": "application/json"}

	# generate url
	url = "http://" + RASPBERRY_PI_IP + ":" + PORT + "/m2m/fim/items/" + DEVICE_UID + "/operations/" + LOCK_OPERATION

	# generate body
	data = json.dumps({"arguments": [operation]})

	# send request
	resp = requests.put(url, auth=(USERNAME, PASSWORD), headers=headers, data=data)

	return resp.text
