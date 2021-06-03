# library imports
import mtcnn
import numpy
from tensorflow.python.keras.models import Model

# project imports
from .face_extract_utils import extract_multiple_faces
from .face_embedding_utils import get_face_embedding
from .candidate_face_check import check_candidate_faces


# recognize faces
def recognize_faces(train_data: numpy.array, detector: mtcnn.MTCNN, model: Model, filename: str = None) -> [str]:

	print("Extracting faces from image...")

	# extract faces of all candidates
	candidate_faces = extract_multiple_faces(detector, filename=filename)

	# check for faces in the image
	if not candidate_faces:
		return ["No faces detected"]

	print("Generating face embeddings...")

	# get face embeddings of all candidates
	candidate_embeddings = [get_face_embedding(face, model) for face in candidate_faces]

	print("Checking faces...")

	# check faces for all candidates
	names = check_candidate_faces(train_data, candidate_embeddings)

	return names
