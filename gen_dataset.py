import numpy as np
import itertools
from scipy.misc import imread
import pandas as pd
from matplotlib import pyplot as plt


# Define a class for the Image.
# Loads image array from the filename specified
# This will handle converting a large image into a smaller one
# with crop_to_ROI based on the centre position and the size specified.
# center is a tuple or array of [row,column] of the ROI center
# crop_size is the height and width of the ROI
# full_image is an array of the image to set the ROI to (should be an RGB array)
class Image:
	def __init__(self, filename):
		self.array = imread(filename)

		self.row_size = self.array.shape[0]
		self.col_size = self.array.shape[1]

	# Removes the bottom of an image to take out any text that appears there
	def crop_img_bottom(self, crop_size=20):
		self.array = self.array[:-crop_size,:,:]

		self.row_size = self.array.shape[0]
		self.col_size = self.array.shape[1]

	# Returns the cropped image to the ROI specified or None if the ROI is not valid
	def crop_to_ROI(self, center, crop_size):
		row_cntr = center[0]
		col_cntr = center[1]

		row_start = row_cntr - (crop_size // 2)
		row_end = row_start + crop_size
		
		col_start = col_cntr - (crop_size // 2)
		col_end = col_start + crop_size

		self.valid_ROI = ( (row_start >= 0)
						and (col_start >= 0)
						and (row_end <= self.row_size-1)
						and (col_end <= self.col_size-1) )

		if self.valid_ROI:
			return self.array[
					row_start:row_end, 
					col_start:col_end, :]
		else:
			return None

# Generates the X and Y for the positive cases as given by ROI_centers locations
def find_positives(image, car_locations):
	crop_size = 40

	X_list = list([])

	for ROI_center in car_locations:
		ROI_image = image.crop_to_ROI(ROI_center, crop_size)

		if image.valid_ROI:
			X_list.append(ROI_image)

	X = np.stack(X_list, axis=0)
	Y = np.ones((X.shape[0],1), int)

	return (X, Y)

# Generates X and Y for the negative cases by scanning chopping the image
# into segments and ignoring the positive cases
def find_negatives(image, car_locations):
	crop_size = 40
	stride = 20
	car_radius = 15

	height_steps = 1 + (image.row_size - crop_size) // stride
	width_steps = 1 + (image.col_size - crop_size) // stride

	ROI_list = list([])

	for i, j in itertools.product(range(height_steps), range(width_steps)):
		row_position = i * stride + (crop_size // 2)
		col_position = j * stride + (crop_size // 2)

		ROI_center = [row_position, col_position]
		dist_to_cars = np.linalg.norm(np.subtract(car_locations, ROI_center),axis=1)

		if np.all(dist_to_cars > car_radius):
			ROI_list.append(ROI_center)

	X_list = list([])

	for ROI_center in ROI_list:
		ROI_image = image.crop_to_ROI(ROI_center, crop_size)

		if image.valid_ROI:
			X_list.append(ROI_image)

	X = np.stack(X_list, axis=0)
	Y = np.zeros((X.shape[0],1), int)

	return (X, Y)

# Saves the X and Y arrays into files to be read with numpy later
def save_arrays(file_number, X, Y):
	x_fname = 'classified_arrays/{}_X.npy'.format(file_number)
	y_fname = 'classified_arrays/{}_Y.npy'.format(file_number)

	np.save(x_fname, X)
	np.save(y_fname, Y)

# The main script
def main(file_number):
	img_fname = 'google_image_dump/{}.png'.format(file_number)
	centres_fname = 'google_image_dump/{}.txt'.format(file_number)

	car_locations = pd.read_csv(centres_fname, sep=',', header=None).values

	image = Image(img_fname)
	image.crop_img_bottom(20)

	(X1, Y1) = find_positives(image, car_locations)
	(X0, Y0) = find_negatives(image, car_locations)

	print('There are {} pictures of cars and {} pictures of not cars'.format(X1.shape[0], X0.shape[0]))

	X = np.concatenate((X1, X0), axis=0)
	Y = np.concatenate((Y1, Y0), axis=0)

	save_arrays(file_number, X, Y)

if __name__ == "__main__":
    # execute only if run as a script
	file_number = input("Enter filename to process (e.g. 12, 79, etc.): ")
	main(file_number)

# import pdb; pdb.set_trace()


