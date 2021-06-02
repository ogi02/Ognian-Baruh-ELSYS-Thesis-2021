# library imports
import mtcnn
import numpy
from PIL import Image
from typing import Tuple
from requests import get
from numpy import asarray
from requests.auth import HTTPDigestAuth

# project constants
from ..constants import *

# image related constants
IMAGE_WIDTH = 160
IMAGE_HEIGHT = 160
REQUIRED_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)


# open image from file
def get_pixels_from_file(filename: str) -> numpy.array:
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
def get_pixels_from_url(url: str = IMAGE_FROM_CAMERA_URL) -> numpy.array:
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
def crop_face(face_box: [int], pixels: numpy.array, required_size: Tuple[int] = REQUIRED_SIZE) -> Image:
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
def extract_single_face(detector: mtcnn.MTCNN, filename: str) -> numpy.array:
	# open the image and get the pixels
	pixels = get_pixels_from_file(filename)

	# detect faces in the image
	face_box = detector.detect_faces(pixels)

	# check if faces are detected
	if len(face_box) == 0:
		return False

	# get cropped image of face
	face_image = crop_face(face_box[0]['box'], pixels)

	return asarray(face_image)


# extract multiple faces from a given image
def extract_multiple_faces(detector: mtcnn.MTCNN, filename: str = None) -> [numpy.array]:
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
