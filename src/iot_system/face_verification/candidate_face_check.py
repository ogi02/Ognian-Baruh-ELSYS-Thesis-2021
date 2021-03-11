from scipy.spatial.distance import cosine

# determine if a candidate face is a match for a known face
def check_candidate_faces(known_embeddings, known_labels, candidate_embeddings, thresh=0.3):

	# list for storing guessed faces
	faces = list()

	for candidate_embedding in candidate_embeddings:
		# reset values
		# i -> counts all known embeddings
		# passed -> counts all passed embeddings
		i = 0
		passed = 0

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

		print(guesses)
		max_passed = 0
		# key -> label
		# value -> times passed
		for key, value in guesses.items():
			if value > max_passed:
				label = key
				max_passed = value

		if max_passed >= 5:
			faces.append(label)

	if not faces:
		return "Unknown"
	else:
		return faces