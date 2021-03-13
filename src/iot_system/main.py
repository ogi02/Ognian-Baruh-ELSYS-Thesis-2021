# library imports
# library imports
from json import loads
from time import sleep
from numpy import load
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace

import paho.mqtt.client as mqtt

# project imports
from face_verification.recognize import recognize_faces
from door_lock_controller.lock_control import lock_door, unlock_door

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
UNKNOWN = "Unknown"
NO_FACES_DETECTED = "No faces detected"

# lock constants
LOCK = "lock"
UNLOCK = "unlock"

# device commands topics
LOCK_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + LOCK_DEVICE_UID
CAMERA_COMMANDS_TOPIC = SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID


# client on connect callback
def client_on_connect(self, userdata, flags, rc):
	# messages for lock
	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + LOCK)

	# messages for unlock
	client.subscribe("command//" + LOCK_COMMANDS_TOPIC + "/req//" + UNLOCK)

	# camera topic
	client.subscribe("e/" + TENANT_ID + "/" + SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID)


# client on message callback
def client_on_message(self, userdata, msg):
	# get message topic
	topic = msg.topic

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

	# if message is from camera for the detected property
	if payload["path"] == "/features/Detector:%2FEventsService%2F1/properties/status/detected" and payload["value"] == True:
		# recognize faces with image from url
		names = recognize_faces(trainData, detector, model)

		print(names)

		# if there are known people
		if names != UNKNOWN and names != NO_FACES_DETECTED:
			# unlock door
			unlock_door()

			# wait 5 seconds
			sleep(5)

			# lock door
			lock_door()


if __name__ == "__main__":

	# load known face embeddings
	data = load(EMBEDDING_FILE, allow_pickle=True)
	trainData = data["trainData"].item()

	# initialize mtcnn detector
	detector = MTCNN()

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# filename = "./test/camera_images/image_3.jpg"
	# filename2 = "./face_verification/exam/exam_gabi_i_kompaniq.jpg"

	# filenames = [
	# 	"./face_verification/exam/exam_balls.jpg",
	# 	"./face_verification/exam/exam_dog.jpg",
	# 	"./face_verification/exam/exam_gabi_i_cveti.jpg",
	# 	"./face_verification/exam/exam_gabi_i_kompaniq.jpg",
	# 	"./face_verification/exam/exam_gabi.jpg",
	# 	"./face_verification/exam/exam_gabi1.jpg",
	# 	"./face_verification/exam/exam_gabi2.jpg",
	# 	"./face_verification/exam/exam_ogi_hacktues.jpg",
	# 	"./face_verification/exam/exam_ogi_i_gabi.jpg",
	# 	"./face_verification/exam/exam_ogi_i_gabi2.jpg",
	# 	"./face_verification/exam/exam_ogi_i_plamen.jpg",
	# 	"./face_verification/exam/exam_ogi.jpg",
	# 	"./face_verification/exam/exam_plamen_i_tedi.jpg",
	# 	"./face_verification/exam/exam_plamen.jpg",
	# 	"./face_verification/exam/exam_random1.jpg",
	# 	"./face_verification/exam/exam_shefa.jpg",
	# 	"./face_verification/exam/exam_tedi.jpg"
	# ]

	# for filename in filenames:

	# 	print(filename)
	# 	# recognize faces
	# 	names = recognize_faces(trainData, detector, model, filename=filename)

	# 	print(names)

	# initialize mqqt client
	client = mqtt.Client("test", None, None, mqtt.MQTTv311)
	client.on_connect = client_on_connect
	client.on_message = client_on_message

	# connect
	client.connect(RASPBERRY_IP, 1883, 60)

	# loop forever
	client.loop_forever()
