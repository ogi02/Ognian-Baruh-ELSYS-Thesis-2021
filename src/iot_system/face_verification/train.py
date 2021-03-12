# library imports
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from numpy import asarray, savez_compressed

# custom functions imports
from face_extract_utils import load_dataset
from face_extract_utils import extract_multiple_faces
from face_embedding_utils import get_face_embedding

MODEL_NAME = "vgg16"
DATASET_FOLDER = "./dataset/"
EMBEDDING_FILE = "../models/embeddings.npz"

def save_embeddings(dictionary):
	# initialize dictionary for train data
	trainData = {}
	
	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# iterate through every known person
	for key, value in dictionary.items():
		# convert each face of that person to a face embedding
		trainData[key] = [get_face_embedding(face_pixels, model) for face_pixels in value]

	# save embeddings and labels to one npz compressed file
	savez_compressed(EMBEDDING_FILE, trainData=trainData)

if __name__ == "__main__":
	# initialize the mtcnn detector
	detector = MTCNN()

	# load training dataset
	dictionary = load_dataset(DATASET_FOLDER, detector)

	# save embeddings
	save_embeddings(dictionary)