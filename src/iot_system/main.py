# library imports
from time import time
from json import loads
from time import sleep
from numpy import load
from requests import get
from mtcnn.mtcnn import MTCNN
from requests.auth import HTTPDigestAuth
from keras_vggface.vggface import VGGFace

import paho.mqtt.client as mqtt

# project imports
from constants import *
from face_verification.recognize import recognize_faces
from door_lock_controller.lock_control import lock_door
from door_lock_controller.lock_control import unlock_door
from camera_controller.screenshot_control import send_screenshot
from notification_controller.notification_control import send_notification

# bosch iot suite constants
TENANT_ID = "ta5c5ad439fe14b32af99092f74e594eb_hub"
SUBSCRIPTION_NAME = "finalyearproj"
NAMESPACE_ID = "iotSystem"

# models constants
MODEL_NAME = "vgg16"
EMBEDDING_FILE = "./models/embeddings.npz"
CASCADE_CLASSIFIER_FILE = "./models/haarcascade_frontalface_default.xml"

# camera constants
UNKNOWN = "Unknown"
NO_FACES_DETECTED = "No faces detected"
GET_SCREENSHOT_COMMAND = "getScreenshot"

# lock constants
LOCK_COMMAND = "lock"
UNLOCK_COMMAND = "unlock"

# device commands topics
LOCK_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + LOCK_DEVICE_UID
CAMERA_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID

# 30000 millis = 30 sec
millis_of_last_operation = 0


# client on connect callback
def client_on_connect(self, userdata, flags, rc):
	# messages for lock
	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + LOCK_COMMAND)

	# messages for unlock
	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + UNLOCK_COMMAND)

	# messages for get screenshot
	client.subscribe("command//" + CAMERA_COMMANDS_TOPIC + "/req//" + GET_SCREENSHOT_COMMAND)

	# camera topic
	client.subscribe("e/" + TENANT_ID + "/" + SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID)

	print("IoT System Initialized!")


# client on message callback
def client_on_message(self, userdata, msg):
	global millis_of_last_operation

	# get message topic
	topic = msg.topic

	# lock door command
	if topic == "command//" + LOCK_COMMANDS_TOPIC + "/req//" + LOCK_COMMAND:
		lock_door()
		return

	# unlock door command
	if topic == "command//" + LOCK_COMMANDS_TOPIC + "/req//" + UNLOCK_COMMAND:
		unlock_door()
		return

	# send screenshot command
	if topic == "command//" + CAMERA_COMMANDS_TOPIC + "/req//" + GET_SCREENSHOT_COMMAND:
		send_screenshot()
		return

	# get payload from message
	payload = loads(msg.payload.decode("utf-8"))

	# if message is from camera for the detected property
	if payload["path"] == "/features/Detector:%2FEventsService%2F1/properties/status/detected" and payload["value"] == True:
		print("Detected!")

		# get now
		millis_now = time() * 1000

		if millis_now - millis_of_last_operation >= 30000:
			# get_image
			image = get(IMAGE_FROM_CAMERA_URL, auth=HTTPDigestAuth(AUTH_USERNAME, AUTH_PASSWORD), stream=True).content

			# recognize faces with image from url
			names = recognize_faces(trainData, detector, model)

			# send notification
			send_notification(names, image)

			# if there are known people
			if names[0] != UNKNOWN and names[0] != NO_FACES_DETECTED:

				# unlock door
				unlock_door()

				# wait 5 seconds
				sleep(5)

				# lock door
				lock_door()

			millis_of_last_operation = time() * 1000


if __name__ == "__main__":

	# load known face embeddings
	data = load(EMBEDDING_FILE, allow_pickle=True)
	trainData = data["trainData"].item()

	# initialize mtcnn detector
	detector = MTCNN()

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# initialize mqtt client
	client = mqtt.Client("iot_system", None, None, mqtt.MQTTv311)
	client.on_connect = client_on_connect
	client.on_message = client_on_message

	# connect
	client.connect(RASPBERRY_PI_IP, 1883, 60)

	# loop forever
	client.loop_forever()
