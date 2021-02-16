# library imports
from numpy import expand_dims
from keras_vggface.vggface import VGGFace
from keras.applications.vgg16 import preprocess_input

# initialize vggface model
model = VGGFace(model='vgg16', include_top=False, input_shape=(224, 224, 3), pooling='avg')

# extract faces and calculate face embeddings for a list of photo files
def get_face_embedding(face_pixels):
	# scale pixel values
	face_pixels = face_pixels.astype('float32')

	# added a 4th dimension so only one face embedding is predicted
	# expected shape from the model is (1, 224, 224, 3)
	samples = expand_dims(face_pixels, axis=0)

	# perform prediction
	prediction = model.predict(samples)
	return prediction[0]
