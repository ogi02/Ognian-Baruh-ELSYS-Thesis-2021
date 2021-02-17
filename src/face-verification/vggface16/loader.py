# library imports
import cv2
from os import mkdir
from sys import exit, argv
from getopt import getopt, GetoptError

path = './dataset/'

def get_name(argv):
	# init first name and last name
	fname = ''
	lname = ''

	# get opts from command line
	try:
		opts, args = getopt.getopt(argv,'f:l:', ["fname=", "lname="])
	# catch error
	except getopt.GetoptError:
		print('Wrong input!')
		exit(1)

	# iterate through opts and get first and last name
	for opt, arg in opts:
		if opt in ('-f', '--fname'):
			fname = arg
		elif opt in ('-l', '--lname'):
			lname = arg

	# get full name
	name = fname + ' ' + lname
	return name

def create_dir(name):
	# create full path
	full_path = path + name

	# create directory
	mkdir(full_path)

	# return new path
	return full_path

def take_screenshots(full_path):
	# init camera
	cam = cv2.VideoCapture(0)
	window_message = "Press space to take a photo or escape to finish!"

	# create window to view the camera
	cv2.namedWindow(window_message, cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_message, 500, 300)

	# init image count
	image_count = 0

	while True:
		# read camera
		# ret -> True or False, depends on whether the read is successful
		# frame -> the frame that is read
		ret, frame = cam.read()

		# if frame read is not successful
		if not ret:
			print("Failed to grab frame!")
			break

		# display window
		cv2.imshow(window_message, frame)

		# wait for key press
		# if argument is 0 -> the frame will be displayed infinitely
		# if argument is 1 -> the frame will be displayed for 1 ms
		key = cv2.waitKey(1)

		# space
		if key % 256 == 32:
			# increment image count
			image_count += 1
			# generate full path for the image
			image_path = full_path + "/image_" + str(image_count) + ".jpg"
			# write the frame at the certain path
			cv2.imwrite(image_path, frame)
			print("Image " + str(image_count) + " written!")

		# escape
		elif key % 256 == 27:
			print("Finishing")
			cv2.destroyAllWindows()
			break

if __name__ == '__main__':
	# call get name without the first keyword argument (loader.py)
	name = get_name(argv[1:])

	# create path to image directory
	full_path = create_dir(name)

	# turn on camera and take screenshots
	take_screenshots(full_path)