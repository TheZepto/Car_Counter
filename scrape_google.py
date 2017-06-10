import requests
import itertools


def main():
	# Google static map image API key must be saved in this file
	api_key = open('api_key.txt', 'r').read()

	# Define lat and long start coords
	lat_start = -27.454560
	long_start = 153.034480
	#Define increments of lat and long
	lat_inc = -0.0007
	long_inc = 0.0009

	# Iterate over the lat and long coords to generate an image grid
	# that is saved in google_image_dump folder
	for i, j in itertools.product(range(10), range(10)):
		latitude = lat_start + (i * lat_inc)
		longitude = long_start + (j * long_inc)

		# Address of map in the format of a .png
		map_address = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=20&size=640x640&maptype=satellite&key={}'.format(
						latitude, longitude, api_key
						)

		# Filename to save the image to
		img_fname = 'google_image_dump\{}{}.png'.format(
						i, j)

		# Open the file and read the web address into it
		f = open(img_fname, 'wb')
		f.write(requests.get(map_address).content)
		f.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()