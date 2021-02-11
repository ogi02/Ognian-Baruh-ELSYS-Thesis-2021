import os
import json
import requests

functionalItemId = 'da:item:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009/Media-0/1:MediaService'
operation = 'getSnapshotUri'
data = {}

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
url = 'http://172.22.150.239:8080/m2m/fim/items/' + functionalItemId + '/operations/' + operation
url = 'http://172.22.150.239:8080/m2m/fim/items/da%3Aitem%3AONVIF%3ABosch-FLEXIDOME_IP_4000i_IR-094454407323822009%2FMedia-0%2F1%3AMediaService/operations/getSnapshotUri'
res = requests.put(url, auth=('admin', 'admin'), headers=headers, data=json.dumps(data))

# print(res)
# print(res.text)

# headers2 = {'Accept': 'application/json'}
# url2 = 'http://172.22.150.239:8080/m2m/fim/items/da%3Adevice%3AONVIF%3ABosch-FLEXIDOME_IP_4000i_IR-094454407323822009/properties'
# res2 = requests.get(url2, auth=('admin', 'admin'), headers=headers2)

body = json.loads(res.text)
# print(body)

image_url = body["result"]
print(image_url)

os.system('python3 recognize.py --url \"{}\"'.format(image_url))
