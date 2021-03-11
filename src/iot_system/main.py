# library imports
import paho.mqtt.client as mqtt

import sys
import time

from json import loads
from numpy import load
from mtcnn.mtcnn import MTCNN
from cv2 import CascadeClassifier
from keras_vggface.vggface import VGGFace

# project imports
from camera_detection.test import take_images_and_recognize
from door_lock_controller.lock_control import lock_door, unlock_door

from face_verification.recognize import recognize_faces

# bosch iot suite constants
TENANT_ID = "ta5c5ad439fe14b32af99092f74e594eb_hub"
SUBSCRIPTION_NAME = "finalyearproj"
NAMESPACE_ID = "iotSystem"
LOCK_DEVICE_UID = "da:device:ZWave:FD72A41B%2F5"
CAMERA_DEVICE_UID = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

# models constants
MODEL_NAME = "vgg16"
EMBEDDING_FILE = "./models/embeddings.npz"
CASCADE_CLASSIFIER_FILE = "./models/haarcascade_frontalface_default.xml"

# raspberry ip
RASPBERRY_IP = "172.22.150.239"

# camera constants
UNKNOWN = "UNKNOWN"
NO_FACES_DETECTED = "No faces detected"

# lock constants
LOCK = "lock"
UNLOCK = "unlock"

# device commands topics
LOCK_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + LOCK_DEVICE_UID
CAMERA_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID

camera_topic = "e/" + TENANT_ID + "/" + SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID

def client_on_connect(self, userdata, flags, rc):
	print("Connected")


	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + LOCK)
	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + UNLOCK)
	# subscribe to camera topic
	# client.subscribe(camera_topic)


def client_on_message(self, userdata, msg):

	# get message topic
	topic = msg.topic
	print(topic)

	# lock door command
	if topic == "command//" + LOCK_COMMANDS_TOPIC + "/req//" + LOCK:
		lock_door()
		return

	# unlock door command
	if topic == "command//" + LOCK_COMMANDS_TOPIC + "/req//" + UNLOCK:
		unlock_door()
		return

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
	trainX, trainY = data["trainX"], data["trainY"]

	# initialize cascade classifier
	classifier = CascadeClassifier(CASCADE_CLASSIFIER_FILE)

	detector = MTCNN()

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# filename = "./test/camera_images/image_3.jpg"
	# filename2 = "./face_verification/exam/exam_gabi_i_kompaniq.jpg"

	filenames = [
		"./face_verification/exam/exam_balls.jpg",
		"./face_verification/exam/exam_dog.jpg",
		"./face_verification/exam/exam_gabi_i_cveti.jpg",
		"./face_verification/exam/exam_gabi_i_kompaniq.jpg",
		"./face_verification/exam/exam_gabi.jpg",
		"./face_verification/exam/exam_gabi1.jpg",
		"./face_verification/exam/exam_gabi2.jpg",
		"./face_verification/exam/exam_ogi_hacktues.jpg",
		"./face_verification/exam/exam_ogi_i_gabi.jpg",
		"./face_verification/exam/exam_ogi_i_gabi2.jpg",
		"./face_verification/exam/exam_ogi_i_plamen.jpg",
		"./face_verification/exam/exam_ogi.jpg",
		"./face_verification/exam/exam_plamen_i_tedi.jpg",
		"./face_verification/exam/exam_plamen.jpg",
		"./face_verification/exam/exam_random1.jpg",
		"./face_verification/exam/exam_shefa.jpg",
		"./face_verification/exam/exam_tedi.jpg",
		"./test/camera_images/image_0.jpg",
		"./test/camera_images/image_1.jpg",
		"./test/camera_images/image_2.jpg",
		"./test/camera_images/image_3.jpg",
		"./test/camera_images/image_4.jpg"
	]

	for filename in filenames:

		print(filename)
		# recognize faces
		names = recognize_faces(filename, trainX, trainY, detector, model)

		print(names)

	# initialize mqqt client
	# client = mqtt.Client("test", None, None, mqtt.MQTTv311)
	# client.on_connect = client_on_connect
	# client.on_message = client_on_message

	# # connect
	# client.connect(RASPBERRY_IP, 1883, 60)

	# # loop forever
	# client.loop_forever()
