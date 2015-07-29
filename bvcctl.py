#!/usr/bin/python
# (C)2015 Brocade Communications Systems, Inc.
# 130 Holger Way, San Jose, CA 95134.
# All rights reserved.
# Author: Gary Berger <gberger@brocade.com>
"""
Brocade SDN Controller - Command Line Interface
Brocade Communications, Inc.

Usage:
        bvcctl [options] <command> [<args>...]

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen

Commands:
             openflow      Perform OpenFlow functions
             show          Retrieve varios elements from BVC
             netconf       Perform NetConf related functions such as retrieve configuration
             http          Perform HTTP based operations
             system        Perform queries on the BVC system itself

"""

import docopt
import requests
from requests.auth import HTTPBasicAuth

import bvcctl.show

# import bvcctl.show

import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class Controller(object):
    def __init__(self, auth, address):
        self.port = auth.get('port', 8181)
        self.auth = HTTPBasicAuth(auth.get('username', 'admin'), auth.get('password', 'admin'))
        self.server = address or auth.get('server')
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}


def main():
    # from bvcctl.common import utils
    argv = ['show']
    args = docopt.docopt(__doc__,argv=argv)
    # args = docopt.docopt(__doc__, version="0.9.0", options_first=True)

    ctl = Controller()


    cmd = args['<command>']
    subcmd = args['<args>']
    commands = [cmd] + subcmd

    module = getattr(bvcctl, cmd)
    module.show_hosts(ctl, commands)
    s = module.__doc__
    a = docopt(s)
    # print arguments

if __name__ == '__main__':
        main()
