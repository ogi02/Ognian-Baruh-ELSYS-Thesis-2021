# library imports
import paho.mqtt.client as mqtt

import sys
import time

from json import loads
from numpy import load
from cv2 import CascadeClassifier
from keras_vggface.vggface import VGGFace

# project imports
from camera_detection.test import take_images_and_recognize
from door_lock_controller.lock_control import lock_door, unlock_door

# bosch iot suite constants
TENANT_ID = "ta5c5ad439fe14b32af99092f74e594eb_hub"
SUBSCRIPTION_NAME = "finalyearproj"
NAMESPACE_ID = "iotSystem"
CAMERA_DEVICE_UID = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

# models constants
MODEL_NAME = "vgg16"
EMBEDDING_FILE = "./models/embeddings.npz"
CASCADE_CLASSIFIER_FILE = "./models/haarcascade_frontalface_default.xml"

# raspberry ip
RASPBERRY_IP = "172.22.150.239"

# camera related values
UNKNOWN = "UNKNOWN"
NO_FACES_DETECTED = "No faces detected"

# topic, where camera sends its messages
camera_topic = "e/" + TENANT_ID + "/" + SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID

def client_on_connect(self, userdata, flags, rc):
	print("Connected")

	# subscribe to camera topic
	client.subscribe(camera_topic)


def client_on_message(self, userdata, msg):
	print("Received message")

	# get payload from message
	payload = loads(msg.payload.decode("utf-8"))

	# if message is detected
	if payload["path"] == "/features/Detector:%2FEventsService%2F1/properties/status/detected" and payload["value"] == True:
		# get names from face verification model with images from camera
		names = take_images_and_recognize(trainX, trainY, classifier, model)

		print(names)

		for name in names:
			if name != UNKNOWN and name != NO_FACES_DETECTED:
				unlock_door()
				time.sleep(3)
				lock_door()

		sys.exit(0)


if __name__ == "__main__":

	# load known face embeddings 
	data = load(EMBEDDING_FILE)
	trainX, trainY = data["arr_0"], data["arr_1"]

	# initialize cascade classifier
	classifier = CascadeClassifier(CASCADE_CLASSIFIER_FILE)

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# initialize mqqt client
	client = mqtt.Client("test", None, None, mqtt.MQTTv311)
	client.on_connect = client_on_connect
	client.on_message = client_on_message

	# connect
	client.connect(RASPBERRY_IP, 1883, 60)

	# loop forever
	client.loop_forever()
