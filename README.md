# Car_Counter
The overall goal of this project is to be able to count the number of cars in a satellite image. The scripts in this project will gather the satellite imagery, assist you in classifying cars in those images, train a convnet to recognise images of cars, and finally analyse a given image to produce a car count.

Details of the project can be found on my blog at http://thezepto.wordpress.com.

### scrape_google.py
This script will gather a 10x10 image array of satellite imagery from Google's Static Maps API.

### gen_datset.py
Assists the user in identifying cars so that a labelled data set can be generated. This data set will then be used to train a convnet.
