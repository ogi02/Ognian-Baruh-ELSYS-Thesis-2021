#!/usr/bin/env python3
# library imports
import time
import numpy as np
from sys import argv, exit
from argparse import ArgumentParser
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine

# custom functions imports
from face_extract_utils import load_dataset
from face_extract_utils import extract_single_face
from face_extract_utils import extract_multiple_faces
from face_embedding_utils import get_face_embedding
 
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

		# dictionary for guesses
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

def recognize_faces(filename, trainX, trainY, start_time):
	# extract faces of all candidates
	candidate_faces = extract_multiple_faces(filename)

	print("2")
	print("--- %s seconds ---" % (time.time() - start_time))

	if not candidate_faces:
		return ['No faces detected']

	# initialize vggface model
	model = VGGFace(model='vgg16', include_top=False, input_shape=(224, 224, 3), pooling='avg')

	print("3")
	print("--- %s seconds ---" % (time.time() - start_time))

	# get face embeddings of all candidates
	candidate_embeddings = list()
	for face in candidate_faces:
		# get face embedding
		candidate_face_embedding = get_face_embedding(face, model)

		# insert face embedding
		candidate_embeddings.append(candidate_face_embedding)

	print("4")
	print("--- %s seconds ---" % (time.time() - start_time))

	# check faces for all candidates
	names = check_candidate_faces(trainX, trainY, candidate_embeddings)

	print("5")
	print("--- %s seconds ---" % (time.time() - start_time))

	return names


if __name__ == '__main__':

	start_time = time.time()

	# get filename from argv
	filename = argv[1]

	# check if filename is given
	if not filename:
		print('Please enter path to image!')
		exit(0)

	# load known face embeddings 
	data = np.load('../vggface16/embeddings.npz')
	trainX, trainY = data['arr_0'], data['arr_1']

	print("1")
	print("--- %s seconds ---" % (time.time() - start_time))

	# perform face recognition
	res = recognize_faces(filename, trainX, trainY, start_time)

	print(res, end='')
