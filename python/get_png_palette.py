#!/usr/bin/python
# Gets the palette used in the pascal voc segmentation images.
# Example:
# $ ./get_png_palette.py
# 0 none [0 0 0]
# 1 aeroplane [128   0   0]
# 2 bicycle [  0 128   0]
# 3 bird [128 128   0]
# 4 boat [  0   0 128]
# 5 bottle [128   0 128]
# 6 bus [  0 128 128]
# 7 car [128 128 128]
# 8 cat [64  0  0]
# 9 chair [192   0   0]
# 10 cow [ 64 128   0]
# 11 diningtable [192 128   0]
# 12 dog [ 64   0 128]
# 13 horse [192   0 128]
# 14 motorbike [ 64 128 128]
# 15 person [192 128 128]
# 16 pottedplant [ 0 64  0]
# 17 sheep [128  64   0]
# 18 sofa [  0 192   0]
# 19 train [128 192   0]
# 20 tvmonitor [  0  64 128]

from PIL import Image
import numpy as np

pascal_classes = [
    'none',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tvmonitor',
]

# The Class version has the above indexes.
# The Object version assigns indexes in order of the object xml. index 1 == object1, index 2 == object 2, ...

im = Image.open("pascal_voc/VOCdevkit/VOC2012/SegmentationClass/2009_000488.png")

palette = im.getpalette()
num_colors = len(palette)/3
palette = np.array(palette).reshape(num_colors, 3)

for i in range(len(pascal_classes)):
    print i, pascal_classes[i], palette[i]
