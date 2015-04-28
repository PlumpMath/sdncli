"""
Usage:
        bvccli http [options] get <uri>
        bvccli http [options] post <uri> <payload>

Options :
            -d --debug             Print JSON dump
            -h --help              This help screen
            -f --force             Ignore cache
            -y --yang              Utilize yang mounted prefix
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""

from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
