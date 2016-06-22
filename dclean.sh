#!/bin/sh
# monitors /caffe/odiddley_home/FI9800P_00626E61E0D6/snap for files from the camera
# Any file found is moved to /caffe/drive_rc/inbound and the userid is fixed.
# In a massive security hole, my_chown is suid root.
m="/caffe/odiddley_home/FI9800P_00626E61E0D6/snap"
d="/caffe/drive_rc/inbound"
while true
do
    find $m -type f -name '*.jpg' |
    while read ffn
    do
        file=`basename $ffn`
        my_chown rgb $ffn
        chgrp rgb $ffn
        mv $ffn $d/$file
    done
    sleep 1
done
