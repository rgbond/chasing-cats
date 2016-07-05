# chasing-cats
Jetson cat chasing: Turn on the lawn sprinkler when a neural net sees a cat.

A collection of utilities useful for working with segmented images
and the fcn variant of Caffe.

    photon:
    cat_sprinkler.cpp       Firmware for the photon
        
    python:
    count_pascal_mat.py     Counts classified pixels in a Pascal Context .mat file
    count_pascal.py         Coutns classified pixels in a Pascal Context .png file
    get_png_palette.py      Gets the pallete from a .png file
    last10.py               Show the last 10 shots from the camera at 1/2 res
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
    tcats.sh                The one I use
    spon                    Disable the sprinkler
    spoff                   Enable the sprinkler
    sprinkle.sh             Start the sprinkler
    sprinkle_off.sh         Stop the sprinkler
    
    src:
    bright.cpp              Brighten images
    cropper.cpp             Crop images to 227 x 227 pixels
    example.cpp             Simple GPU example used to debug opencv builds
    snapshots.cpp           Convert a movie to single frames

    fcn:                    Modified files from the Shellhammer github
    infer.py                Saves a file in addition to processing a file
    batch_infer.py          Processes a bunch of files from the command line
    tbatch_infer.py         The one I use to process inbound cat images
    voc-fcn32s:
        deploy.prototxt     A deployment version of trainval.prototxt
