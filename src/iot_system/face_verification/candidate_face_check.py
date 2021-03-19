from statistics import mean
from scipy.spatial.distance import cosine

def check_candidate_faces(trainData, candidate_embeddings, threshold=0.3):
	'''
	trainData {
		"Person 1": [emb1, emb2, emb3, ...]
		"Person 2": [emb1, emb2, emb3, ...]
	}
	where "emb1" stands for face embedding 1

	"key, value in trainData.items()" gets:
	key -> name of the person
	value -> list of face embeddings for that person

	"for known in value" gets:
	known -> every face embedding of a certain person
	value -> list of face embeddings for that person

	"for candidate in candidate_embeddings" gets:
	candidate -> candidate face embedding
	candidate_embeddings -> list of all face embeddings of candidates

	"cosine" gets the cosine of the candidate and 1 known face embedding

	"mean" gets the mean of all the consines for 1 known person (10 values)

	if there is only one face:
	scores: 
		[{'Person 1': 0.20623254179954528, 'Person 2': 0.401296055316925}]

	if there are more than one faces:
	scores:
		[
			{'Person 1': 0.20623254179954528, 'Person 2': 0.40129605531692521},
			{'Person 1': 0.51230716642703621, 'Person 2': 0.26734365280065493}
		]
	'''

	# get scores
	scores = [{key: mean(cosine(known, candidate) for known in value) for key, value in trainData.items()} for candidate in candidate_embeddings]

	names = []
	# iterate through the scores for every candidate
	for score_dict in scores:
		# iterate through the every known person
		for name, score in score_dict.items():
			# if is the same person
			if score < threshold:
				# append name
				names.append(name)

	# if candidates faces don't match
	if not names:
		return ["Unknown"]

	return names