# library imports
from PIL import Image
from time import time
from requests import get
from google.cloud import storage
from google.cloud import firestore
from requests.auth import HTTPDigestAuth

# image constants
# CAMERA_IP = "172.22.173.47" # office
CAMERA_IP = "192.168.2.41" # home
# CAMERA_IP = "..." # thesis
AUTH_USERNAME = "service"
AUTH_PASSWORD = "Admin!234"
IMAGE_FROM_CAMERA_URL = "http://" + CAMERA_IP + "/snap.jpg?JpegCam=1"

# camera uid
CAMERA_DEVICE_UID = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

# bucket constants
BUCKET_ID = "iot-home-system-7dab8.appspot.com"
IMAGES_ON_DEMAND_FOLDER_NAME = "imagesOnDemand"


# open image from url
def open_image_from_url():
	# retrieve image from url
	resp = get(IMAGE_FROM_CAMERA_URL, auth=HTTPDigestAuth(AUTH_USERNAME, AUTH_PASSWORD), stream=True)
	# resp = get(IMAGE_2, stream=True)

	# return raw image data
	return resp.content


# send image to cloud storage
def send_image_to_cloud_storage():
	# get image data
	image_data = open_image_from_url()

	# init storage client
	client = storage.Client()

	# get bucket
	bucket = client.get_bucket(BUCKET_ID)

	# create blob
	blob = bucket.blob(IMAGES_ON_DEMAND_FOLDER_NAME + "/" + CAMERA_DEVICE_UID + "/image_on_demand.jpg")

	# upload image
	blob.upload_from_string(
		image_data,
		content_type='image/jpg'
	)

# send update message to firestore
def send_time_of_image_to_firestore():
	# init firestore client
	db = firestore.Client()

	# get document
	doc_ref = db.collection(u'user_devices').document(u'xjMJgd3PP8XuGwlpdrBRnUf0ThC3').collection(u'cameras').document(u'LlI2EAybxztHMtt7ooGq')

	# get now time
	now = round(time() * 1000)

	# update values
	doc_ref.update({
		u'time': now
	})

# send screenshot
def send_screenshot():
	# send screenshot to firebase cloud storage
	send_image_to_cloud_storage()

	# send update to firestore
	send_time_of_image_to_firestore()
