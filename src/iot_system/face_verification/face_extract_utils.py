# library imports
import requests
from PIL import Image
from io import BytesIO
from os import listdir
from numpy import asarray
from os.path import isdir
from requests.auth import HTTPDigestAuth

IMAGE_WIDTH = 160
IMAGE_HEIGHT = 160
REQUIRED_SIZE = [IMAGE_WIDTH, IMAGE_HEIGHT]
ALLOWED_EXTENSIONS = ".png", ".jpg", ".jpeg"

# detect all faces in an image
def get_pixels(filename):
	# open the image from file
	image = Image.open(filename)

	# convert to RGB if image is black and white
	image = image.convert("RGB")

	# convert image to numpy array
	# numpy array is a 3 dimensional array
	# the first dimension is the width of the image
	# the second dimension is the height of the image
	# the third dimension is the color of the pixel (RGB)
	pixels = asarray(image)

	return pixels

# extract a single face from a given image
def extract_single_face(filename, classifier, required_size=REQUIRED_SIZE):
	# open the image and get the pixels
	pixels = get_pixels(filename)

	# detect faces in the image
	face_box = classifier.detectMultiScale(pixels)

	# check if faces are detected
	if not face_box:
		return False

	# get beginning coordinates of face
	x1, y1, width, height = face_box[0]

	# get end coordinates of face
	x2, y2 = x1 + width, y1 + height

	# crop face from image
	face = pixels[y1:y2, x1:x2]

	# resize the image
	image = Image.fromarray(face)
	image = image.resize(required_size)

	return asarray(image)

# extract a single face from a given image
def extract_multiple_faces(filename, classifier, required_size=REQUIRED_SIZE):
	# open the image and get the pixels
	pixels = get_pixels(filename)

	# detect faces in the image
	faces_boxes = classifier.detectMultiScale(pixels)

	# check if faces are detected
	if not faces_boxes:
		return False

	faces = list()
	# extract every face from the image
	for face_box in faces_boxes:
		# get beginning coordinates of face
		x1, y1, width, height = face_box

		# get end coordinates of face
		x2, y2 = x1 + width, y1 + height

		# crop face from image
		face_pixels = pixels[y1:y2, x1:x2]

		# resize the image
		image = Image.fromarray(face_pixels)
		image = image.resize(required_size)

		# return face array
		faces.append(asarray(image))

	return faces

# load the faces from a directory
def load_faces(directory, classifier):
	faces = list()

	# iterate through all files
	for filename in listdir(directory):
		# make sure that the file is an image
		if not filename.lower().endswith(ALLOWED_EXTENSIONS):
			continue

		# get full path of image
		image_path = directory + filename

		# extract face
		face = extract_single_face(image_path, classifier)

		# append face to the list of faces if face iss detected
		if face.any():
			faces.append(face)

	return faces

# load the whole dataset
def load_dataset(directory, classifier):
	x, y = list(), list()

	# iterate through all subdirectories in the dataset aka all the people in the dataset
	for subdir in listdir(directory):
		# create full path
		subdir_path = directory + subdir + "/"

		# skip files (error check)
		if not isdir(subdir_path):
			continue

		# load all the faces for that person
		faces = load_faces(subdir_path, classifier)

		# create labels for all the faces of that person
		labels = [subdir for _ in range(len(faces))]

		# store faces and labels
		x.extend(faces)
		y.extend(labels)

	return asarray(x), asarray(y)
