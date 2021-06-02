# library imports
import mtcnn
import numpy
from sys import exit
from os import listdir
from os.path import isdir
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from numpy import savez_compressed

# project imports
from face_extract_utils import extract_single_face
from face_embedding_utils import get_face_embedding

MODEL_NAME = "vgg16"
DATASET_FOLDER = "./dataset/"
EMBEDDING_FILE = "../models/embeddings.npz"

ALLOWED_EXTENSIONS = ".png", ".jpg", ".jpeg"


# load the faces from a directory
def load_faces(directory: str, detector: mtcnn.MTCNN) -> [numpy.array]:
	faces = []

	# iterate through all files
	for filename in listdir(directory):
		# make sure that the file is an image
		if not filename.lower().endswith(ALLOWED_EXTENSIONS):
			continue

		# get full path of image
		image_path = directory + filename

		# extract face
		face = extract_single_face(detector, image_path)

		# check is face is detected
		if face is False:
			print("The face detection model didn't detect a face in {} in {}".format(filename, directory))
			exit(1)

		# append face to the list of faces if face is detected
		faces.append(face)

	return faces


# load the whole dataset
def load_dataset(directory: str, detector: mtcnn.MTCNN) -> {str, [numpy.array]}:
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


def save_embeddings(dataset: {str, [numpy.array]}):
	# initialize dictionary for train data
	train_data = {}

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# iterate through every known person
	for key, value in dataset.items():
		# convert each face of that person to a face embedding
		train_data[key] = [get_face_embedding(face_pixels, model) for face_pixels in value]

	# save embeddings and labels to one npz compressed file
	savez_compressed(EMBEDDING_FILE, train_data=train_data)


if __name__ == "__main__":
	# initialize the mtcnn detector
	mtcnn_detector = MTCNN()

	# load training dataset
	image_dataset = load_dataset(DATASET_FOLDER, mtcnn_detector)

	# save embeddings
	save_embeddings(image_dataset)
