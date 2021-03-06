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
    coord_rects = []
    first_coord = []
    temp_shapes = []

    def drawbox(x, y, colour='white', width=1, size=80):
        # Draws a rectangle around the x, y position
        nonlocal canvas
        x0 = x - size//2
        x1 = x0 + size
        y0 = y - size//2
        y1 = y0 + size
        id = canvas.create_rectangle(x0, y0, x1, y1,
                                     width=width, outline=colour)
        return id

    def drawcircle(x, y, colour='white', width=1, size=80):
        # Draws a circle around the x, y position
        nonlocal canvas
        x0 = x - size//2
        x1 = x0 + size
        y0 = y - size//2
        y1 = y0 + size
        id = canvas.create_oval(x0, y0, x1, y1, width=width, outline=colour)
        return id

    def tempshape(event):
        nonlocal canvas, temp_shapes, first_coord
        x1 = event.x
        y1 = event.y
        # Log the first coord
        if not first_coord:
            first_coord.append(x1)
            first_coord.append(y1)
        # Remove the last shape(s)
        if temp_shapes:
            for shape in temp_shapes:
                canvas.delete(shape)
        # Draw the new shape(s)
        x0 = first_coord[0]
        y0 = first_coord[1]
        x = (x0 + x1) / 2
        y = (y0 + y1) / 2
        size = ((x0-x1)**2 + (y0-y1)**2)**0.5
        temp_shapes.append(drawcircle(x, y, colour='white', size=size))

    def logcoords(event):
        # Append the x, y click coords to coords list
        nonlocal coords, coord_rects, temp_shapes, first_coord, scale
        x1 = event.x
        y1 = event.y
        x0 = first_coord[0]
        y0 = first_coord[1]
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2
        # Remove the temporary rectangle
        if temp_shapes:
            for shape in temp_shapes:
                canvas.delete(shape)
            temp_shapes = []
            first_coord = []
        # Draw a rectangle around the coords
        rect_id = drawbox(x, y, colour='green', width=2)
        # Scale x and y coords to row column of original image
        column = x // scale
        row = y // scale
        # Record the coords and rect id to the lsit
        coords.append((row, column))
        coord_rects.append(rect_id)

    def removelastcoord(event):
        nonlocal canvas, coords, coord_rects
        # Pop last coord and rect id from list
        rect_id = coord_rects.pop()
        coords.pop()
        # Delete the rectangle
        canvas.delete(rect_id)

    # Bind left click motion to draw a temporary rectangle
    canvas.bind("<B1-Motion>", tempshape)
    # Bind release left click to log the coord
    canvas.bind("<ButtonRelease-1>", logcoords)
    # Bind right click to remove the last coord
    canvas.bind("<Button-3>", removelastcoord)

    root.geometry("+10+10")  # Open window 10px offset from top left corner
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
