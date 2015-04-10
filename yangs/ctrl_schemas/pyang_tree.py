
import glob
import subprocess
from subprocess import call

first = True
outfile = "pyang_tree.txt"
for f in glob.glob('*.yang'):
    if (first):
        cmd = "pyang -f tree "+f+" > "+ outfile 
        first = False
    else:
        cmd = "pyang -f tree "+f+" >> "+ outfile 
    print cmd
    subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=True)
