'''
This script will download a 10x10 array of satellite images using the Google
Static Map API and store them to the google_image_dump folder. The images are
from Brisbane as given by the lat_start and long_start coords.

Pre-requisties:
- Have your Google Static Map API key in a text file called api_key.txt
- Have a folder named google_image_dump
'''

import requests
import itertools
import os

from S3Archive import S3Archive


def main():
    s3archive = S3Archive(
        archive_name='GoogleMapsImages',
        bucket_name='zepto-archive',
        add_datetime_to_name=True
    )
    # Google static maps API key must be stored in api_key.txt
    api_key = open('api_key.txt', 'r').read()

    # Define start positions for the lat and log
    lat_start = -27.458462
    long_start = 153.035735
    # Define the lat and long increments - this depends on the start lat and long
    lat_inc = -0.0007
    long_inc = 0.0009

    # Iterate over a 10x10 grid and capture satellite images
    for i, j in itertools.product(range(10), range(10)):
        latitude = lat_start + (i * lat_inc)
        longitude = long_start + (j * long_inc)

        # Generate the Google maps URL
        map_address = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=20&size=640x640&maptype=satellite&key={}'.format(
                        latitude, longitude, api_key
                        )

        # Specify the filename to save the png to in the google_image_dump folder
        img_fname = os.path.join('google_image_dump', '{}{}.png'.format(i, j))

        # Fetch the image at the URL and save it to the filename
        with open(img_fname, 'wb') as f:
            f.write(requests.get(map_address).content)

        s3archive.addfile(img_fname)

    s3archive.create()

if __name__ == "__main__":
    # execute only if run as a script
    main()