# library imports
import random
import string
from time import time
from json import dumps
from typing import Union
from requests import post
from google.cloud import storage
from google.cloud import firestore

# project imports
from constants import *

# bucket constants
BUCKET_ID = "iot-home-system-7dab8.appspot.com"
NOTIFICATION_IMAGES_FOLDER_NAME = "notificationImages"

# cloud messaging
CLOUD_MESSAGING_TARGET_URL = "https://fcm.googleapis.com/fcm/send"
CLOUD_MESSAGING_SERVER_KEY = "AAAAemxd5oU:APA91bE1VUxwA5cjWFA2j5IlFfR0a7dxNZL6gWRgxBprpTEx7SgoJAAQcXkP_e-VF310lvAf5DDNPp8aFd_qUzyT-HFvlwsr-1spILwWotuel5E2lkgoLmOT9ZALZTXyf6vkvDsw4Bcx"


# send image to cloud storage
def send_image_to_cloud_storage(image_name: str, image_data: bytes) -> None:
	# init storage client
	client = storage.Client()

	# get bucket
	bucket = client.get_bucket(BUCKET_ID)

	# create blob
	blob = bucket.blob(NOTIFICATION_IMAGES_FOLDER_NAME + "/" + CAMERA_DEVICE_UID + "/" + image_name + ".jpg")

	# upload image
	blob.upload_from_string(
		image_data,
		content_type="image/jpg"
	)


# send update message to firestore
def send_update_to_firestore(notification_id: str, names: [str], timestamp: time) -> None:
	# init firestore client
	db = firestore.Client()

	# get document reference
	doc_ref = db.collection(u"notifications").document(notification_id)

	# update values
	doc_ref.set({
		u"time": timestamp,
		u"names": names,
		u"camera_uid": CAMERA_DEVICE_UID,
		u"notification_id": notification_id
	})


# send notification through cloud messaging service
def send_cloud_notification(names: [str], timestamp: time) -> Union[None, bool]:
	# init firestore client
	db = firestore.Client()

	# get document reference
	doc_ref = db.collection(u"camera_ownership").document(CAMERA_DEVICE_UID)

	# get document
	doc = doc_ref.get()
	if not doc.exists:
		return False

	# get dictionary with values from document
	values = doc.to_dict()

	# initialize headers for requests
	headers = {
		"Authorization": "key=" + CLOUD_MESSAGING_SERVER_KEY,
		"Content-Type": "application/json"
	}

	# initialize body for requests
	body = {
		"collapse_key": "New message",
		"priority": "high",
		"notification": {
			"title": names,
			"body": timestamp
		}
	}

	for phone_id in values["phone_ids"]:
		# add phone id to body
		body["to"] = phone_id

		# send post request to firebase cloud messaging service
		post(CLOUD_MESSAGING_TARGET_URL, headers=headers, data=dumps(body))


# send notification
def send_notification(names: [str], image: bytes) -> None:
	# get now time
	now = round(time() * 1000)

	# generate notification id
	notification_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))

	# send image to firebase cloud storage
	send_image_to_cloud_storage(notification_id, image)

	# send update message to cloud firestore
	send_update_to_firestore(notification_id, names, now)

	# send cloud notification
	send_cloud_notification(names, now)
