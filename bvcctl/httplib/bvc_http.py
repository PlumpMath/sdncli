"""
Usage:
        bvccli http [options] get <resource>
        bvccli http [options] delete <resource>
        bvccli http [options] post <resource> ([--payload <payload>] | [--file <file>])
        bvccli http [options] put <resource> ([--payload <payload>] | [--file <file>])

Options :
            -d --debug             Print JSON dump
            -h --help              This help screen
            -f --force             Ignore cache
            -y --yang              Utilize yang mounted prefix
            -o --operational       Read from operational datastore
            -p --operations        RPC Resource
            -c --config            Read from configuration datastore
            -s --streams           Read from streams

            Resources:
            opendaylight-inventory:nodes/node/{node}/yang-ext:mount

"""

from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
