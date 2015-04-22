"""
Usage:
        bvccli show [options] hosts
        bvccli show [options] nodes
        bvccli show [options] modules

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -v --verbose           Add verbose output
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""

from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
