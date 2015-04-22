"""
Usage:
        bvccli system [options] memory
        bvccli system [options] heap
        bvccli system [options] gc

Options :
            -d --debug             Print JSON dump
            -v --verbose           Add verbose output
            -h --help              This help screen

"""

from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
