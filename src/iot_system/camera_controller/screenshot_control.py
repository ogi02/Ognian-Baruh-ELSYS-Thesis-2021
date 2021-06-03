# library imports
from time import time
from requests import get
from google.cloud import storage
from google.cloud import firestore
from requests.auth import HTTPDigestAuth

# project imports
from iot_system.constants import *

# bucket constants
BUCKET_ID = "iot-home-system-7dab8.appspot.com"
IMAGES_ON_DEMAND_FOLDER_NAME = "imagesOnDemand"


# open image from url
def open_image_from_url() -> bytes:
	# retrieve image from url
	resp = get(IMAGE_FROM_CAMERA_URL, auth=HTTPDigestAuth(AUTH_USERNAME, AUTH_PASSWORD), stream=True)

	# return raw image data
	return resp.content


# send image to cloud storage
def send_image_to_cloud_storage() -> None:
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
		content_type="image/jpg"
	)


# send update message to firestore
def send_time_of_image_to_firestore() -> None:
	# init firestore client
	db = firestore.Client()

	# get document
	doc_ref = db.collection(u"user_devices").document(u"xjMJgd3PP8XuGwlpdrBRnUf0ThC3").collection(u"cameras").document(
		u"LlI2EAybxztHMtt7ooGq")

	# get now time
	now = round(time() * 1000)

	# update values
	doc_ref.update({
		u"time": now
	})


# send screenshot
def send_screenshot() -> None:
	# send screenshot to firebase cloud storage
	send_image_to_cloud_storage()

	# send update to firestore
	send_time_of_image_to_firestore()
