import numpy as np
import itertools
from scipy.misc import imread
import pandas as pd
from matplotlib import pyplot as plt

# Define a class for region of interest (ROI).
# This will handle converting a large image into a smaller one
# based on the centre position and the size specified.
# center is a tuple or array of [row,column] of the ROI center
# crop_size is the height and width of the ROI
# full_image is an array of the image to set the ROI to (should be an RGB array)
class ROI:
	def __init__(self, center, crop_size, full_image):
		self.row_cntr = center[0]
		self.col_cntr = center[1]
		self.crop_size = crop_size
		self.full_image = full_image

		self.row_start = row_cntr - (crop_size // 2)
		self.row_end = row_start + crop_size
		
		self.col_start = col_cntr - (crop_size // 2)
		self.col_end = col_start + crop_size

	def in_image(self):
		# Checks if the ROI is contained within the bounds of the image
		if self.row_start < 0:
			return False
		if self.col_start < 0:
			return False
		if self.row_end > self.full_image.shape[0]-1:
			return False
		if self.col_end > self.full_image.shape[2]-1:
			return False
		return True

	def crop_to(self):
		# Performs the crop and returns the cropped image 
		return self.full_image[
					self.row_start:self.row_end, 
					self.col_start:self.col_end, :]

# Removes the bottom of an image to take out any text that appears there
def crop_img_bottom(img_array, crop_size=40):
	return img_array[:-crop_size,:,:]

# Generates the X and Y for the positive cases as given by ROI_centers locations
def find_positives(image, ROI_centers):
	
	return (X, Y)

# Generates X and Y for the negative cases by scanning chopping the image
# into segments and ignoring the positive cases
def find_negatives(image, ROI_centers):

	return (X, Y)
	

def save_arrays(file_number, X, Y):
	x_fname = 'classified_arrays\{}_X.npy'.format(img_number)
	y_fname = 'classified_arrays\{}_Y.npy'.format(img_number)

	np.save(x_fname, X)
	np.save(y_fname, Y)


def main():
	file_number = input("Enter filename to process (e.g. 12, 79, etc.): ")
	img_fname = 'google_image_dump/{}.png'.format(file_number)
	centres_fname = 'google_image_dump/{}.txt'.format(file_number)

	image = imread(img_fname)
	ROI_centers = pd.read_csv(centres_fname, sep=',', header=None).values

	image = crop_img_bottom(full_image, 20)

	(X1, Y1) = find_positives(full_image, ROI_centers)

	(X0, Y0) = find_negatives(full_image, ROI_centers)

	X = np.concatenate((X1,X0), axis=)
	Y = np.concatenate((Y1,Y0), axis=)

	save_arrays(img_number, X, Y)

if __name__ == "__main__":
    # execute only if run as a script
    main()


# import pdb; pdb.set_trace()