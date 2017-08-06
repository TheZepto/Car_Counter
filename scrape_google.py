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
import sys

from Archive import Archive
from S3 import S3Bucket


def main():
    # Google static maps API key must be stored in api_key.txt
    api_key = open('api_key.txt', 'r').read()

    # Define start positions for the lat and log
    lat_start = -27.458462
    long_start = 153.035735
    # Define the lat and long increments - this depends on the start position
    lat_inc = -0.0007
    long_inc = 0.0009

    # Make a file list to add to an archive and upload to S3
    file_list = []

    # Iterate over a 10x10 grid and capture satellite images
    for i, j in itertools.product(range(10), range(10)):
        latitude = lat_start + (i * lat_inc)
        longitude = long_start + (j * long_inc)

        # Generate the Google maps URL
        map_address = ('https://maps.googleapis.com/maps/api/staticmap?' +
                       'center={},{}'.format(latitude, longitude) +
                       '&zoom=20&size=640x640' +
                       '&maptype=satellite&key={}'.format(api_key))

        # Specify the directory and filename to save the png to
        directory = 'google_image_dump'
        if not os.path.exists(directory):
            os.makedirs(directory)
        img_fname = os.path.join('google_image_dump', '{}{}.png'.format(i, j))

        # Fetch the image at the URL and save it to the filename
        with open(img_fname, 'wb') as f:
            f.write(requests.get(map_address).content)

        file_list.append(img_fname)

    # Build an archive with the image files
    archive = Archive(file_list)
    buffer = archive.streamtargz()
    # Upload the archive to the zepto-archive bucket in S3
    s3bucket = S3Bucket('zepto-archive')
    s3bucket.uploadstream(buffer, archive.name)

if __name__ == "__main__":
    # execute only if run as a script
    main()
