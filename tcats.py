#!/usr/bin/python
# Usage: show_seg src.jpg seg.png 
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
labels = ["none", "truck_0", "truck_22.5", "truck_45", "truck_67.5",
          "truck_90", "truck_112.5", "truck_135", "truck_157.5",
          "truck_180", "truck_202.5", "truck_225", "truck_247.5",
          "truck_270", "truck_292.5", "truck_315", "truck_337.5",
          "cat", "dog", "person"]

# Turn the sprinkler on these guys
sprinkle_list = ["cat", "dog"]

# Keep these images around in outbound/item
keep_list = ["truck_0", "truck_22.5", "truck_45", "truck_67.5",
             "truck_90", "truck_112.5", "truck_135", "truck_157.5",
             "truck_180", "truck_202.5", "truck_225", "truck_247.5",
             "truck_270", "truck_292.5", "truck_315", "truck_337.5",
             "cat", "dog", "person"]

def get_list(png_fn):
    im = Image.open(png_fn)
    histo = im.histogram()
    indices = []
    items = []
    counts = []
    for i in range(256):
        if histo[i] > 0:
            indices += [i]
            items += [labels[i]]
            counts += [histo[i]]
    return indices, items, counts

while True:
    flist = os.listdir(classified)
    flist.sort()
    if flist == None or len(flist) < 2:
        time.sleep(0.25)
        continue
    while len(flist) > 2:
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
        jpeg_full_dest = p.join(raw, jpeg_fn)
        png_full_dest = p.join(raw, png_fn)
        os.rename(jpeg_full_src, jpeg_full_dest)
        os.rename(png_full_src, png_full_dest)
        indices, items, counts = get_list(png_full_dest)
        log_line = jpeg_fn + ' '
        num_items = len(items)
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
        with open(count_log, "a") as log:
            log.write(log_line + '\n')
        # spawn and forget
        subprocess.Popen(["mask_out.py", jpeg_full_dest, png_full_dest])
