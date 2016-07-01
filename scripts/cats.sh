#!/bin/bash
# Simple minded script that starts up caffe and runs batch_infer.py when a set of
# images appear in the inbound dirctory. This is simple but not the best to use
# because you are penalized the cost of the startup on each bacth of files.
# See tcats.sh for a better approach
cd /caffe/fcn*
echo "starting declean.sh"
dclean.sh &
date > caffe.out
while true
do
    find /caffe/drive_rc/inbound -type f -name '*.jpg' -print | sort > tmp1
    if [ -s tmp1 ]
    then
        echo running caffe
        ./batch_infer.py `cat tmp1` >> caffe.out 2>&1
        cat tmp1 |
        while read yard
        do
            result=`echo $yard | sed s/.jpg$/.png/`
            pascal_histo $result > tmp2
            mask_out.py $yard $result
            ybn=`basename $yard`
            ydn=/caffe/drive_rc/outbound/raw/$ybn
            rbn=`basename $result`
            rdn=/caffe/drive_rc/outbound/raw/$rbn
            echo $ybn `cat tmp2` >> counts.out
            mv $yard $ydn
            mv $result $rdn
            cat tmp2 |
            while read line
            do
                i=`echo $line | awk '{print $1}'`
                case "$i" in
                    cat|bird)
                        ln $ydn /caffe/drive_rc/outbound/$i
                        ln $rdn /caffe/drive_rc/outbound/$i
                        echo "keeping $ybn: $i"
                        hr=`date +%H`
                        if [ $hr -lt 8 ] || [ $hr -ge 20 ]
                        then
                            date
                            echo "running sprinkler"
                            /caffe/drive_rc/photon/sprinkle.sh
                        fi
                        ;;
                    aeroplane|bicycle|boat|bottle|bus|car|chair|\
                    table|dog|horse|motorbike|person|sofa|train|tvmonitor)
                        ln $ydn /caffe/drive_rc/outbound/$i
                        ln $rdn /caffe/drive_rc/outbound/$i
                        echo "keeping $ybn: $i"
                        ;;
                    none|pottedplant|sheep|cow|\
                    *)
                        echo "skipping $ybn: $i"
                        ;;
                esac
            done
        done
        echo "Files processed"
    fi
    sleep 1
done
