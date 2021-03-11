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

def save_embeddings(trainX, trainY):
	newTrainX = list()

	# initialize vggface model
	model = VGGFace(model=MODEL_NAME, include_top=False, input_shape=(160, 160, 3), pooling="avg")

	# convert each face in the train set to an embedding
	for face_pixels in trainX:
		embedding = get_face_embedding(face_pixels, model)
		newTrainX.append(embedding)

	# convert list to np array
	newTrainX = asarray(newTrainX)

	# save embeddings and labels to one npz compressed file
	savez_compressed(EMBEDDING_FILE, trainX=newTrainX, trainY=trainY)

# initialize the mtcnn detector
detector = MTCNN()

# load training dataset
trainX, trainY = load_dataset(DATASET_FOLDER, detector)

# save embeddings
save_embeddings(trainX, trainY)