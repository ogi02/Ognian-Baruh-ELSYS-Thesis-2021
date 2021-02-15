# library imports
import requests
from PIL import Image
from io import BytesIO
from os import listdir
from numpy import asarray
from os.path import isdir
from mtcnn.mtcnn import MTCNN
from requests.auth import HTTPDigestAuth

# init the detector
detector = MTCNN()

# detect all faces in an image
def get_pixels(filename):
	# open the image from file
	image = Image.open(filename)

	# convert to RGB if image is black and white
	image = image.convert('RGB')

	# convert image to numpy array
	# numpy array is a 3 dimensional array
	# the first dimension is the width of the image
	# the second dimension is the height of the image
	# the third dimension is the color of the pixel (RGB)
	pixels = asarray(image)

	return pixels

# extract a single face from a given image
def extract_single_face(filename, required_size=(224, 224)):
	# open the image and get the pixels
	pixels = get_pixels(filename)

	# detect faces in the image
	results = detector.detect_faces(pixels)

	# check if faces are detected
	if not results:
		return False

	# get the first face (only face) 
	face = results[0]

	# get beginning coordinates of face
	x1, y1, width, height = face['box']

	# happened twice, some error
	x1, y1 = abs(x1), abs(y1)

	# get end coordinates of face
	x2, y2 = x1 + width, y1 + height

	# crop face from image
	face = pixels[y1:y2, x1:x2]

	# resize the image
	image = Image.fromarray(face)
	image = image.resize(required_size)

	return asarray(image)

# extract a single face from a given image
def extract_multiple_faces(filename, required_size=(224, 224)):
	# open the image and get the pixels
	pixels = get_pixels(filename)

	# detect faces in the image
	results = detector.detect_faces(pixels)

	# check if faces are detected
	if not results:
		return False

	faces = list()
	# extract every face from the image
	for face in results:
		# get beginning coordinates of face
		x1, y1, width, height = face['box']

		# happened twice, some error
		x1, y1 = abs(x1), abs(y1)

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
def load_faces(directory):
	faces = list()

	# iterate through all files
	for filename in listdir(directory):
		# make sure that the file is an image
		if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
			continue

		# get full path of image
		image_path = directory + filename

		# extract face
		face = extract_single_face(image_path)

		# append face to the list of faces if face iss detected
		if face:
			faces.append(face)

	return faces

# load the whole dataset
def load_dataset(directory):
	x, y = list(), list()

	# iterate through all subdirectories in the dataset aka all the people in the dataset
	for subdir in listdir(directory):
		# create full path
		subdir_path = directory + subdir + '/'

		# skip files (error check)
		if not isdir(subdir_path):
			continue

		# load all the faces for that person
		faces = load_faces(subdir_path)

		# create labels for all the faces of that person
		labels = [subdir for _ in range(len(faces))]

		# store faces and labels
		x.extend(faces)
		y.extend(labels)

	return asarray(x), asarray(y)
