import numpy as np
import itertools
from scipy.misc import imread
from matplotlib import pyplot as plt

def crop_img(img_array, crop_size=40):
	img_array = img_array[:-crop_size,:,:]

	return img_array

def make_training_data(img_array):
	size = 40
	stride = 20

	height = img_array.shape[0]
	width = img_array.shape[1]

	height_steps = (height - size) // stride
	width_steps = (width - size) // stride

	total_imgs = height_steps * width_steps

	x_train = np.zeros([total_imgs, size, size, 3], dtype=np.uint8)

	i = 0

	for y, x in itertools.product(range(height_steps), range(width_steps)):
		img = img_array[y*stride:y*stride+size, x*stride:x*stride+size, :]
		x_train[i,:,:,:] = img
		i += 1

	return x_train

def classify_training(x_train):
	total_imgs = x_train.shape[0]

	y_train = np.zeros([total_imgs, 1], dtype=np.uint8)
	
	plt.ion()
	plt.figure()
	
	for i in range(total_imgs):
		img = x_train[i,:,:,:]
		plt.clf()
		plt.imshow(img)
		plt.draw()
		plt.pause(0.01)
		classify = input("If the image is a car press 1: ")
		if classify == '1':
			y_train[i,:] = 1.

	print('This set had {} images of cars.'.format(np.sum(y_train)))

	return y_train

def save_arrays(img_number, x_train, y_train):
	x_fname = 'classified_arrays\{}_X.npy'.format(img_number)
	y_fname = 'classified_arrays\{}_Y.npy'.format(img_number)

	np.save(x_fname, x_train)
	np.save(y_fname, y_train)


def main():
	img_number = input("Enter filename to process (e.g. 12, 79, etc.): ")
	img_fname = 'google_image_dump\{}.png'.format(img_number)

	img_array = imread(img_fname)

	img_array = crop_img(img_array, 40)

	x_train = make_training_data(img_array)
	
	y_train = classify_training(x_train)

	save_arrays(img_number, x_train, y_train)

if __name__ == "__main__":
    # execute only if run as a script
    main()