#!/usr/bin/python
# zips together the neg directory with a single file for the segmenation
# Usage zip_dir.py neg_dir ext neg_seg.png

import sys
import os
import os.path as p

if len(sys.argv) == 4:
    d1 = sys.argv[1]
    ext = sys.argv[2]
    neg = sys.argv[3]

    if not p.exists(d1):
        print "Bad directory name"
        exit(1)
    if not p.exists(neg):
        print "Bad neg seg"
        exit(1)

    full_fn2 = p.abspath(neg)

    if not p.exists(full_fn2):
        print "oops:", full_fn2
        exit(1)

    d1 = p.abspath(d1)
    d1_files = os.listdir(d1)
    d1_files.sort()

    for f in d1_files:
        fn1_base = p.basename(f)
        fn1, fn1_ext = p.splitext(fn1_base)
        if fn1_ext != ext:
            continue
        full_fn1 = p.join(d1, fn1 + ext) 
        if not p.exists(full_fn1):
            print "oops:", full_fn1
            exit(1)
        print full_fn1, full_fn2
