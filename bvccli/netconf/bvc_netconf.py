"""
Usage:
        bvccli netconf [options] mount <node> <address> <username> <password> [--port <port>] [--mlx]
        bvccli netconf [options] mounts
        bvccli netconf [options] unmount <node>
        bvccli netconf [options] config <node>
        bvccli netconf [options] capabilities <node>
        bvccli netconf [options] schemas <node>
        bvccli netconf [options] schema <node> <resource>

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen
            -o --operationa        Read from operational datastore
            -c --config            Read from configuration datastore

"""

from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
