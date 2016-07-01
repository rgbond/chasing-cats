#!/usr/bin/python
# Usage: tcats..py
# Processes files that have been segmented by the FCN network
# Get the labels for the segmented items, saves the images we care about
# turns on the sprinkler for cats and dogs
#

import sys
import os
import os.path as p
import subprocess
import time

from PIL import Image
import numpy as np
import cv2

# Cats have to be bigger than this
smallest_blob = 1400

# Has a set of jpegs and pngs processed by tbatch_infer.py
classified = "/caffe/drive_rc/classified"
# Where the files go next
outbound = "/caffe/drive_rc/outbound"
raw = p.join(outbound, "raw")
# How to kick off the photon
sprinkle = "/home/rgb/bin/sprinkle.sh"
# Log file for the counts
count_log = "/caffe/fcn.berkeleyvision.org/counts.out"

# Labels for everything the neural net can recognize. Indexes matter in this list
labels = [ "none", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
           "cow", "table", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
           "train", "tvmonitor"]

# Turn the sprinkler on these guys
sprinkle_list = ["cat", "dog"]

# Keep these images around in outbound/item
keep_list = ["cat", "dog", "person"]

def get_list(png_fn):
    im = Image.open(png_fn)
    histo = im.histogram()
    indices = []
    items = []
    counts = []
    for i in range(len(labels)):
        if histo[i] > 0:
            indices += [i]
            items += [labels[i]]
            counts += [histo[i]]
    return indices, items, counts

while True:
    # Get a list of files
    flist = os.listdir(classified)
    flist.sort()
    if flist == None or len(flist) < 2:
        time.sleep(0.25)
        continue
    while len(flist) > 2:
        # Should be a .jpg and a .png with matching file names
        jpeg_fn = flist.pop(0)
        jpeg_full_src = p.join(classified, jpeg_fn)
        jpeg_base, jpeg_ext = p.splitext(jpeg_fn)
        if jpeg_ext != ".jpg":
            print "ignoring strange file: ", jpeg_fn
            os.remove(jpeg_full_src)
            continue
        png_fn = flist.pop(0)
        png_full_src = p.join(classified, png_fn)
        png_base, png_ext = p.splitext(png_fn)
        if png_ext != ".png" or jpeg_base != png_base:
            print "ignoring strange file pair ", jpeg_fn, png_fn
            os.remove(jpeg_full_src)
            os.remove(png_full_src)
            continue
        # Figure out where to save the images - everything goes to outbound/raw
        jpeg_full_dest = p.join(raw, jpeg_fn)
        png_full_dest = p.join(raw, png_fn)
        # Move to outbound/raw
        os.rename(jpeg_full_src, jpeg_full_dest)
        os.rename(png_full_src, png_full_dest)
        # Find the segmented pixels
        indices, items, counts = get_list(png_full_dest)
        log_line = jpeg_fn + ' '
        num_items = len(items)
        # Do something with items we care about
        for i in range(num_items):
            index = indices[i]
            item = items[i]
            count = counts[i]
            if item in sprinkle_list:
                if "person" not in items and count > smallest_blob:
                    subprocess.call(sprinkle)
            if item in keep_list:
                dest_dir = p.join(outbound, item)
                os.link(jpeg_full_dest, p.join(dest_dir, jpeg_fn))
                os.link(png_full_dest, p.join(dest_dir, png_fn))
                print jpeg_fn, "keeping", item, count
            else:
                print jpeg_fn, "skipping", item, count
            log_line += item + " " + str(index) + " " + str(count)
            if i < num_items - 1:
                log_line += " "
        # Log it
        with open(count_log, "a") as log:
            log.write(log_line + '\n')
        # spawn and forget a process to convert the png to a file we can see
        subprocess.Popen(["mask_out.py", jpeg_full_dest, png_full_dest])
