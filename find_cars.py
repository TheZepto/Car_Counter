import numpy as np
import itertools
from matplotlib import pyplot as plt
from scipy.misc import imread

import keras
from keras.models import load_model

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

def get_cropped_images(image):
	crop_size = 40
	stride = 1

	height_steps = 1 + (image.row_size - crop_size) // stride
	width_steps = 1 + (image.col_size - crop_size) // stride

	ROI_list = list([])

	for i, j in itertools.product(range(height_steps), range(width_steps)):
		row_position = i * stride + (crop_size // 2)
		col_position = j * stride + (crop_size // 2)

		ROI_list.append([row_position, col_position])

	X_list = list([])
	ROI_centers = list([])

	for ROI_center in ROI_list:
		ROI_image = image.crop_to_ROI(ROI_center, crop_size)

		if image.valid_ROI:
			X_list.append(ROI_image)
			ROI_centers.append(ROI_center)

	X = np.stack(X_list, axis=0)
	ROI = np.array(ROI_centers)

	return X, ROI

def main():
	model = load_model('saved_models/model.70-0.05.hdf5')

	img = Image('test_images/04.png')
	img.crop_img_bottom(20)

	X, ROI = get_cropped_images(img)

	y_prob = model.predict(X)

	prob_map = np.zeros((img.row_size,img.col_size))
	iteration = 0
	for i, j in ROI:
		prob_map[i,j] = y_prob[iteration, 1]
		iteration += 1

	# y_hat = np.argmax(y_prob, axis=1)
	plt.figure()
	plt.imshow(img.array)
	plt.imshow(prob_map, alpha=0.4, cmap='BuPu')
	plt.show()

if __name__ == "__main__":
	# execute only if run as a script
	main()