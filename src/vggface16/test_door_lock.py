import json
import requests

host = "172.22.150.239"
port = "8080"
deviceuid = "da:item:ZWave%2FFD72A41B%2F5:secure%2FC7E4BE6C8D78D27ECA253BF0DF3C5F7CCA187241%2F0x62%2FZWaveDoorLock"
operation = "setMode"

unlocked = 0
locked = 255

# set locked or unlocked
mode = locked

headers = {"Accept": "application/json", "Content-Type": "application/json"}
url = "http://" + host + ":" + port + "/m2m/fim/items/" + deviceuid + "/operations/" + operation
data = json.dumps({"arguments": [mode]})

resp = requests.put(url, auth=("admin", "admin"), headers=headers, data=data)

print(resp)