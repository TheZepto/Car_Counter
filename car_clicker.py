import glob
import os
from tkinter import *
from PIL import Image, ImageTk
import csv

from Archive import Archive
from S3 import S3Bucket


def carclicker(fname, scale=2):  
    # Loading the image
    org_image = Image.open(fname)
    width, height = org_image.size
    width *= scale
    height *= scale
    org_image = org_image.resize((width, height))  # resize image

    # Setting up a tkinter canvas with image on it
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    img = ImageTk.PhotoImage(org_image)
    canvas.create_image(0, 0, image=img, anchor="nw")

    coords = []

    def logcoords(event):
        # Append the x, y click coords to coords list
        nonlocal coords, scale
        x = event.x
        y = event.y

        drawbox(x, y)

        column = x // 2
        row = y // 2

        coords.append((row, column))

    def drawbox(x, y):
        # Draws a rectangle around the x, y position
        nonlocal canvas
        size = 80
        x0 = x - size//2
        x1 = x0 + size
        y0 = y - size//2
        y1 = y0 + size
        canvas.create_rectangle(x0, y0, x1, y1, width=2, outline='white')

    # Bind left click on mouse to logcoords
    canvas.bind("<Button 1>", logcoords)

    root.mainloop()

    return coords


def main():
    dat_file_list = []

    img_files = glob.glob('google_image_dump/*.png')

    for img_file in img_files:
        coords = carclicker(img_file)

        dat_file = img_file + '.dat'
        with open(dat_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(coords)

        dat_file_list.append(dat_file)

    archive = Archive(dat_file_list)
    buffer = archive.streamtargz()

    s3bucket = S3Bucket('zepto-archive')
    s3bucket.uploadstream(buffer, archive.name)


if __name__ == "__main__":
    # execute only if run as a script
    main()
