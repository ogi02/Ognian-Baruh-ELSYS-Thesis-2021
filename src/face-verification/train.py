# library imports
from numpy import asarray, savez_compressed
from keras_vggface.vggface import VGGFace

# custom functions imports
from face_extract_utils import load_dataset
from face_extract_utils import extract_multiple_faces
from face_embedding_utils import get_face_embedding

def save_dataset(trainX, trainY):
	# save faces and labels to one npz compressed file
	savez_compressed('dataset.npz', trainX, trainY)

def save_embeddings(trainX, trainY):
	newTrainX = list()

	# initialize model
	model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

	# convert each face in the train set to an embedding
	for face_pixels in trainX:
		embedding = get_face_embedding(model, face_pixels)
		newTrainX.append(embedding)

	# convert list to np array
	newTrainX = asarray(newTrainX)

	# save embeddings and labels to one npz compressed file
	savez_compressed('embeddings.npz', newTrainX, trainY)

# load training dataset
trainX, trainY = load_dataset('./dataset/')

# save face dataset
save_dataset(trainX, trainY)

# save embeddings
save_embeddings(trainX, trainY)
