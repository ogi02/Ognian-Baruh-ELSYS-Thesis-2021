# library imports
import paho.mqtt.client as mqtt

from cv2 import CascadeClassifier
from keras_vggface.vggface import VGGFace

# project imports
from camera_detection.test import take_images_and_recognize

# bosch iot suite constants
TENANT_ID = "ta5c5ad439fe14b32af99092f74e594eb_hub"
SUBSCRIPTION_NAME = "finalyearproj"
NAMESPACE_ID = "test1"
CAMERA_DEVICE_UID = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

# raspberry ip
RASPBERRY_IP = "172.22.150.239"

# topic, where camera sends its messages
camera_topic = "e/" + TENANT_ID + "/" + SUBSCRIPTION_NAME + ":" + NAMESPACE_ID + ":" + CAMERA_DEVICE_UID

def client_on_connect(self, userdata, flags, rc):
	print("Connected")

	# subscribe to camera topic
	client.subscribe(camera_topic)


def client_on_message(self, userdata, msg):
	print("Received message")

	# get payload from message
	payload = json.loads(msg.payload.decode("utf-8"))

	# if message is detected
	if payload["path"] == "/features/Detector:%2FEventsService%2F1/properties/status/detected" and payload["value"] == True:
		take_images_and_recognize(trainX, trainY, classifier, model)


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