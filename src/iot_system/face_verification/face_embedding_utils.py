# library imports
from numpy import expand_dims
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input

# extract faces and calculate face embeddings for a list of photo files
def get_face_embedding(face_pixels, model):
	# scale pixel values
	face_pixels = face_pixels.astype("float32")

	# added a 4th dimension so only one face embedding is predicted
	# expected shape from the model is (1, 224, 224, 3)
	samples = expand_dims(face_pixels, axis=0)

	# prepare the face for the model, e.g. center pixels
	samples = preprocess_input(samples, version=2)

	# perform prediction
	prediction = model.predict(samples)
	return prediction[0]
