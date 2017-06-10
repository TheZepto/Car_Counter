import requests
import itertools

def main():
	api_key = open('api_key.txt', 'r').read()
	lat_start = -27.458462
	long_start = 153.035735

	lat_inc = -0.0007
	long_inc = 0.0009

	for i, j in itertools.product(range(10), range(10)):
		latitude = lat_start + (i * lat_inc)
		longitude = long_start + (j * long_inc)
		

		map_address = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=20&size=640x640&maptype=satellite&key={}'.format(
						latitude, longitude, api_key
						)

		img_fname = 'google_image_dump\{}{}.png'.format(
						i, j)

		f = open(img_fname, 'wb')
		f.write(requests.get(map_address).content)
		f.close()

if __name__ == "__main__":
	# execute only if run as a script
	main()