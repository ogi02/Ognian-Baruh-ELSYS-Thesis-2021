from os import mkdir
from sys import argv
from sys import exit
from PIL import Image
from time import sleep
from requests import get
from os.path import exists
from requests.auth import HTTPDigestAuth

path_name = '../camera-detection/camera_images/'

def get_image_from_url(url, number):
	# get image from url
	resp = get(url, auth=HTTPDigestAuth('service', 'Admin!234'), stream=True)

	# open image
	image = Image.open(resp.raw)

	# convert to RGB if needed
	image = image.convert('RGB')

	# save image
	image = image.save('{}/exam_{}.jpg'.format(path_name, number))

if __name__ == '__main__':
	# check if url is not given
	if len(argv) < 2:
		print('URL is required! Exiting..')
		exit(0)

	# get url from command line
	url = argv[1]

	# create directory for images if it doesn't exist
	if not exists(path_name):
		mkdir(path_name)

	# create images
	for i in range(10):
		sleep(0.1)
		get_image_from_url(url, i + 1)
