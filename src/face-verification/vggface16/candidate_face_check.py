from scipy.spatial.distance import cosine

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