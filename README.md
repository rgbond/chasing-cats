# chasing-cats
Jetson cat chasing

A collection of utilities useful for working with segmented images
and the fcn variant of Caffe.

    python:
    count_pascal_mat.py     Counts classified pixels in a Pascal Context .mat file
    count_pascal.py         Coutns classified pixels in a Pascal Context .png file
    get_png_palette.py      Gets the pallete from a .png file
    mask_out.py             Masks out and colorizes the classified pixels in an image
    mat2png.py              Convert a Pascal Context .mat file to .png
    movie.py                Spin through a bunch of images on the command line
    png2mat.py              Convert a Pascal Context .png file to .mat
    resize.py               Resize an image
    seg_fix.py              Demo for how to change the segmentation in a file
    show_seg.py             Overlays displays a base image with the semented pixels
    yesno.py                Sort a bunch of images into "yes" and "no" buckets
    zip_dir.py              Zip two directories together
    zip_neg.py              Zip a directory with a single file
    
    scripts:
    cats.sh                 Simple script to run fcn segmentations on files coming in from FTP
    dclean.sh               Monitor an FTP directory
    
    src:
    bright.cpp              Brighten images
    cropper.cpp             Crop images to 227 x 227 pixels
    example.cpp             Simple GPU example used to debug opencv builds
    snapshots.cpp           Convert a movie to single frames
