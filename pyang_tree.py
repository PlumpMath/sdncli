#!/usr/bin/python
import glob
import subprocess
import sys
from subprocess import call

first = True
outfile = "pyang_tree.txt"
for f in glob.glob(sys.argv[1] + '/*.yang'):
    if (first):
        cmd = "pyang -f tree -p " + sys.argv[1] + " " +f+" > " + outfile
        first = False
    else:
        cmd = "pyang -f tree -p " + sys.argv[1] + " " +f+" >> " + outfile
    print cmd
    subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=True)
