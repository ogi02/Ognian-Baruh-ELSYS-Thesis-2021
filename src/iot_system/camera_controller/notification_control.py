# library imports
import random
import string

from PIL import Image
from time import time
from requests import get
from google.cloud import storage
from google.cloud import firestore

# image constants
CAMERA_IP = "172.22.173.47"
AUTH_USERNAME = "service"
AUTH_PASSWORD = "Admin!234"
IMAGE_1 = "https://filedn.com/ltOdFv1aqz1YIFhf4gTY8D7/ingus-info/BLOGS/Photography-stocks3/stock-photography-slider.jpg"
IMAGE_2 = "https://images.unsplash.com/photo-1494253109108-2e30c049369b?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTN8fHJhbmRvbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&w=1000&q=80"

# camera uid
CAMERA_DEVICE_UID = "da:device:ONVIF:Bosch-FLEXIDOME_IP_4000i_IR-094454407323822009"

# bucket constants
BUCKET_ID = "iot-home-system-7dab8.appspot.com"
NOTIFICATION_IMAGES_FOLDER_NAME = "notificationImages"


# send image to cloud storage
def send_image_to_cloud_storage(image_name, image_data):
	# init storage client
	client = storage.Client()

	# get bucket
	bucket = client.get_bucket(BUCKET_ID)

	# create blob
	blob = bucket.blob(NOTIFICATION_IMAGES_FOLDER_NAME + "/" + CAMERA_DEVICE_UID + "/" + image_name + ".jpg")

	# upload image
	blob.upload_from_string(
		image_data,
		content_type='image/jpg'
	)

# send update message to firestore
def send_notification_to_firestore(notification_id, names):
	# init firestore client
	db = firestore.Client()

	# get document
	doc_ref = db.collection(u'notifications').document(notification_id)

	# get now time
	now = round(time() * 1000)

	# update values
	doc_ref.set({
		u'time': now,
		u'names': names,
		u'camera_uid': CAMERA_DEVICE_UID,
		u'notification_id': notification_id
	})

# send notification
def send_notification(names, image):
	# generate notification id
	notification_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))

	# send image to firebase cloud storage
	send_image_to_cloud_storage(notification_id, image)

	# send update message to cloud firestore
	send_notification_to_firestore(notification_id, names)

# image = get(IMAGE_2, stream=True).content

# send_notification(["Ognian Baruh", "Gabriela Yoncheva"], image)
# send_notification(["Unknown"], image)
# send_notification(["No faces detected"], image)
