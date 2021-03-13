# library imports
import requests
from sys import exit
from PIL import Image
from io import BytesIO
from os import listdir
from numpy import asarray
from os.path import isdir
from mtcnn.mtcnn import MTCNN

# image related constants
IMAGE_WIDTH = 160
IMAGE_HEIGHT = 160
REQUIRED_SIZE = [IMAGE_WIDTH, IMAGE_HEIGHT]
ALLOWED_EXTENSIONS = ".png", ".jpg", ".jpeg"

# camera url constants
CAMERA_IP = "172.22.173.47"
AUTH_USERNAME = "service"
AUTH_PASSWORD = "Admin!234"
IMAGE_FROM_CAMERA_URL = "http://" + CAMERA_IP + "/snap.jpg?JpegCam=1"


# open image from file
def get_pixels_from_file(filename):
	# open the image from file
	image = Image.open(filename)

	# convert to RGB if image is grayscale
	image = image.convert("RGB")

	# convert image to numpy array
	# numpy array is a 3 dimensional array
	# the first dimension is the width of the image
	# the second dimension is the height of the image
	# the third dimension is the color of the pixel (RGB)
	pixels = asarray(image)

	return pixels


# open image from url
def get_pixels_from_url(url=IMAGE_FROM_CAMERA_URL):
	# retrieve image from url
	resp = get(url, auth=HTTPDigestAuth(AUTH_USERNAME, AUTH_PASSWORD), stream=True)

	# get image from response
	image = Image.open(resp.raw)

	# convert to RGB if image is grayscale
	image = image.convert("RGB")

	# convert image to numpy array
	# numpy array is a 3 dimensional array
	# the first dimension is the width of the image
	# the second dimension is the height of the image
	# the third dimension is the color of the pixel (RGB)
	pixels = asarray(image)

	return pixels


# crop face from image
def crop_face(face_box, pixels, required_size=REQUIRED_SIZE):
	# get beginning coordinates, width and height of face
	x1, y1, width, height = face_box

	# error handling
	x1, y1 = abs(x1), abs(y1)

	# get end coordinates of face
	x2, y2 = x1 + width, y1 + height

	# crop face from image
	face = pixels[y1:y2, x1:x2]

	# create face image
	face_image = Image.fromarray(face)

	# resize the image to required size
	face_image = face_image.resize(required_size)

	return face_image


# extract a single face from a given image
def extract_single_face(filename, detector):
	# open the image and get the pixels
	pixels = get_pixels(filename)

	# detect faces in the image
	face_box = detector.detect_faces(pixels)

	# check if faces are detected
	if len(face_box) == 0:
		return False

	# get cropped image of face
	face_image = crop_face(face_box[0]['box'], pixels)

	return asarray(face_image)


# extract multiple faces from a given image
def extract_multiple_faces(detector, filename=None, required_size=REQUIRED_SIZE):
	# if filename is given
	if filename is not None:
		# open image from file
		pixels = get_pixels_from_file(filename)
	else:
		# open image from url
		pixels = get_pixels_from_url()

	# detect faces in the image
	faces_boxes = detector.detect_faces(pixels)

	# check if faces are detected
	if len(faces_boxes) == 0:
		return False

	faces = []
	# extract every face from the image
	for face_box in faces_boxes:
		# get cropped image of face
		face_image = crop_face(face_box['box'], pixels)

		# append image to face array
		faces.append(asarray(face_image))

	return faces


# load the faces from a directory
def load_faces(directory, detector):
	faces = []

	# iterate through all files
	for filename in listdir(directory):
		# make sure that the file is an image
		if not filename.lower().endswith(ALLOWED_EXTENSIONS):
			continue

		# get full path of image
		image_path = directory + filename

		# extract face
		face = extract_single_face(image_path, detector)

		# check is face is detected
		if face is False:
			print("The face detection model didn't detect a face in {} in {}".format(filename, directory))
			exit(1)

		# append face to the list of faces if face is detected
		faces.append(face)

	return faces


# load the whole dataset
def load_dataset(directory, detector):
	dictionary = {}

	# iterate through all subdirectories in the dataset aka all the people in the dataset
	for subdir in listdir(directory):
		# create full path
		subdir_path = directory + subdir + "/"

		# skip files (error check)
		if not isdir(subdir_path):
			continue

		# load all the faces for that person
		faces = load_faces(subdir_path, detector)

		# add faces with label to dictionary
		dictionary[subdir] = faces

	return dictionary
