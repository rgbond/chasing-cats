#!/usr/bin/python
# zips together two directories
# Usage zip_dir.py d1 d2 ext1 ext2

import sys
import os
import os.path as p

if len(sys.argv) == 5:
    d1 = sys.argv[1]
    d2 = sys.argv[2]
    ext1 = sys.argv[3]
    ext2 = sys.argv[4]

    if not p.exists(d1) or not p.exists(d2):
        print "Bad diretory neames"
        exit(1)
    d1 = p.abspath(d1)
    d2 = p.abspath(d2)

    d1_files = os.listdir(d1)

    for f in d1_files:
        fn1_base = p.basename(f)
        fn1, fn1_ext = p.splitext(fn1_base)
        if fn1_ext != ext1:
            continue
        full_fn1 = p.join(d1, fn1 + ext1) 
        if not p.exists(full_fn1):
            print "oops:", full_fn1
            exit(1)
        full_fn2 = p.join(d2, fn1 + ext2)
        if not p.exists(full_fn2):
            continue
        print full_fn1, full_fn2
