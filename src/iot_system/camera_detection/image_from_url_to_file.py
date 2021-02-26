#!/usr/bin/env python3

# library imports
from sys import argv
from sys import exit
from PIL import Image
from time import sleep
from requests import get
from requests.auth import HTTPDigestAuth

# auth constants
AUTH_USERNAME = "service"
AUTH_PASSWORD = "Admin!234"
IMAGES_PATH = "./camera_images/"

def get_image_from_url(url, number):
	# get image from url
	resp = get(url, auth=HTTPDigestAuth(AUTH_USERNAME, AUTH_PASSWORD), stream=True)

	# open image
	image = Image.open(resp.raw)

	# convert to RGB if needed
	image = image.convert("RGB")

	# save image
	image = image.save("{}/image_{}.jpg".format(path_name, number))

if __name__ == "__main__":
	# check if url is not given
	if len(argv) < 2:
		print("URL is required! Exiting..")
		exit(0)

	# get url from command line
	url = argv[1]

	# create images
	for i in range(5):
		sleep(0.1)
		get_image_from_url(url, i)
