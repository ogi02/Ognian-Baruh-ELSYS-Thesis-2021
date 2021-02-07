# library imports
import numpy as np
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine

# custom functions imports
from face_extract_utils import load_dataset
from face_extract_utils import extract_single_face
from face_extract_utils import extract_multiple_faces
from face_embedding_utils import get_face_embedding

from os import listdir
 
# determine if a candidate face is a match for a known face
def check_candidate_faces(known_embeddings, known_labels, candidate_embeddings, thresh=0.5):

	# list for storing guessed faces
	faces = list()

	for candidate_embedding in candidate_embeddings:
		# reset values
		# i -> counts all known embeddings
		# passed -> counts all passed embeddings
		# label -> name of candidate ('Unknown' by default)
		i = 0
		passed = 0
		label = 'Unknown'

		# guesses dictionary
		guesses = {label: 0 for label in known_labels}

		# iterate through known face embeddings
		for known_embedding in known_embeddings:
			# get score
			score = cosine(known_embedding, candidate_embedding)

			# check if candidate embedding passes the threshold
			if score <= thresh:
				guesses[known_labels[i]] += 1

			i += 1


		label = 'Unknown'
		max_passed = 0
		# key -> label
		# value -> times passed
		for key, value in guesses.items():
			if value > max_passed:
				label = key
				max_passed = value

		if max_passed >= 20 and label not in faces:
			faces.append(label)

	if not faces:
		faces.append('Unknown')

	return faces

def test_multiple_faces(filename, model, trainX, trainY):
	# extract faces of all candidates
	candidate_faces = extract_multiple_faces(filename)

	# get face embeddings of all candidates
	candidate_embeddings = list()
	for face in candidate_faces:
		# get face embedding
		candidate_face_embedding = get_face_embedding(model, face)

		# insert face embedding
		candidate_embeddings.append(candidate_face_embedding)

	names = check_candidate_faces(trainX, trainY, candidate_embeddings)

	print('---------------------------')
	print('Filename: {}'.format(filename))
	print('Guess: {}'.format(names))

# load known face embeddings 
data = np.load('embeddings.npz')
trainX, trainY = data['arr_0'], data['arr_1']

# initialize vggface model
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

# define filename
# filename = './exam/exam_ogi.jpg'
directory = './exam/'

# iterate through all files
for file in listdir(directory):
	# make sure that the file is an image
	if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
		continue

	# get filename
	filename = directory + file

	test_multiple_faces(filename, model, trainX, trainY)

print('---------------------------\n')