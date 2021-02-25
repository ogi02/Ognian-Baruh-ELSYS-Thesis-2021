# library imports
import paho.mqtt.client as mqtt

from os import exists
from numpy import load
from shutil import rmtree
from os.path import exists
from subprocess import call

# project imports
from face_verification.recognize import recognize_faces

# models constants
MODEL_NAME = "vgg16"
EMBEDDING_FILE = "./models/embeddings.npz"
CASCADE_CLASSIFIER_FILE = "./models/haarcascade_frontalface_default.xml"

# path constants
CAMERA_IMAGES_PATH = "./camera_images"
IMAGE_FROM_CAMERA_URL = "http://172.22.172.33/snap.jpg?JpegCam=1"
IMAGE_FROM_URL_SCRIPT = "../camera_detection/image_from_url_to_file.py"

def take_images_and_recognize(trainX, trainY, classifier, model):
	# remove folder for camera images if it exists
	if exists(CAMERA_IMAGES_PATH):
		rmtree(CAMERA_IMAGES_PATH)

	# create folder for camera images
	mkdir(CAMERA_IMAGES_PATH)

	# get photos from camera and save them
	subprocess.call([IMAGE_FROM_URL_SCRIPT, IMAGE_FROM_CAMERA_URL])

	for i in range(5):
		# generate image name
		image_name = CAMERA_IMAGES_PATH + "/image_{}.jpg".format(i)

		# recognize faces
		names = recognize_faces(image_name, trainX, trainY, classifier, model)

		# print result
		print(names)


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
