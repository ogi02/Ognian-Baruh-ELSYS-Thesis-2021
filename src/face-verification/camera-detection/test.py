#!/usr/bin/env python3
import os
import sys
import json
import requests
import subprocess

import paho.mqtt.client as mqtt

from numpy import load
from shutil import rmtree
from os.path import exists
from cv2 import CascadeClassifier
from keras_vggface.vggface import VGGFace

from vggface16.recognize import recognize_faces

#b"{
#"topic":"finalyearproj/test1:da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009/things/twin/commands/modify","headers":{"
#response-required":false,"correlation-id":"5aa6ab40-09ed-4291-951c-0f3b26bcf878"},"path":"/features/Detector:%2FEventsService%2F1/properties/status/detected","value":true}"

tenant_id = "ta5c5ad439fe14b32af99092f74e594eb_hub"
subscription = "finalyearproj"
namespace = "test1"
device_uid = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

topic = "e/" + tenant_id + "/" + subscription + ":" + namespace + ":" + device_uid

def client_on_connect(self, userdata, flags, rc):
	print("Connected")
	client.subscribe(topic)


def client_on_message(self, userdata, msg):
	print("Received message")
	payload = json.loads(msg.payload.decode("utf-8"))
	print(payload["path"])
	print(payload["value"])
	if payload["path"] == "/features/Detector:%2FEventsService%2F1/properties/status/detected" and payload["value"] == True:

		if exists("./camera_images"):
			rmtree("./camera_images")

		subprocess.call(["../face-verification/image_from_url_to_file.py", "http://172.22.172.33/snap.jpg?JpegCam=1"])

		for i in range(10):
			output = subprocess.check_output([sys.executable, "../face-verification/recognize.py", "./camera_images/image_{}.jpg".format(i)])
			names = output.decode("utf-8")
			print(names)

		client.disconnect()
		sys.exit(0)


if __name__ == "__main__":

	# load known face embeddings 
	data = load('./models/embeddings.npz')
	trainX, trainY = data['arr_0'], data['arr_1']

	# initialize cascade classifier
	classifier = CascadeClassifier('./models/haarcascade_frontalface_default.xml')

	# initialize vggface model
	model = VGGFace(model='vgg16', include_top=False, input_shape=(160, 160, 3), pooling='avg')

	# # initialize mqqt client
	# client = mqtt.Client("test", None, None, mqtt.MQTTv311)
	# client.on_connect = client_on_connect
	# client.on_message = client_on_message

	# # connect
	# client.connect("172.22.150.239", 1883, 60)

	# # loop forever
	# client.loop_forever()

	print("ready")
	a = input()

	filename = "./vggface16/exam/exam_ogi.jpg"

	# perform face recognition
	res = recognize_faces(filename, trainX, trainY, classifier, model)

	print(res, end='')


# functionalItemId = "da:item:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009/Media-0/1:MediaService"
# operation = "getSnapshotUri"
# data = {}

# headers = {"Accept": "application/json", "Content-Type": "application/json"}
# url = "http://172.22.150.239:8080/m2m/fim/items/" + functionalItemId + "/operations/" + operation
# url = "http://172.22.150.239:8080/m2m/fim/items/da%3Aitem%3AONVIF%3ABosch-FLEXIDOME_IP_4000i_IR-094454407323822009%2FMedia-0%2F1%3AMediaService/operations/getSnapshotUri"
# res = requests.put(url, auth=("admin", "admin"), headers=headers, data=json.dumps(data))

# # print(res)
# # print(res.text)

# # headers2 = {"Accept": "application/json"}
# # url2 = "http://172.22.150.239:8080/m2m/fim/items/da%3Adevice%3AONVIF%3ABosch-FLEXIDOME_IP_4000i_IR-094454407323822009/properties"
# # res2 = requests.get(url2, auth=("admin", "admin"), headers=headers2)

# body = json.loads(res.text)
# # print(body)

# image_url = body["result"]
# print(image_url)

# os.system("python3 recognize.py --url \"{}\"".format(image_url))
