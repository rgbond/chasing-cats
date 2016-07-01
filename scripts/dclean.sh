#!/bin/sh
# monitors the ftp directory for innbound images
# Any file found gets the permissions fixed and moved to /caffe/inbound
m="/caffe/camera_home/FI9800P_00626E61E0D6/snap"
d="/caffe/inbound"
while true
do
    find $m -type f -name '*.jpg' |
    while read ffn
    do
        file=`basename $ffn`
        chmod 644 $ffn
        mv $ffn $d/$file
    done
    sleep 1
done
