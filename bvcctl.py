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

from docopt import docopt
from pybvc.controller.controller import Controller
from pybvc.common.status import STATUS
import bvcctl.show
import bvcctl.node
from requests import ConnectionError
from logging import log


import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logging.propagate = True
# requests_log = logging.getLogger("requests")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class Session(Controller):
    def __init__(self, ip, port, user, password):
        try:
            Controller.__init__(self, ip, port, user, password)
        except Exception, e:
            raise e
        result = self.build_inventory_object()
        if(result.status.eq(STATUS.OK)):
            self.inventory = result.data
            result = self.build_topology_object("flow:1")
            if(result.status.eq(STATUS.OK)):
                self.topology = result.data



def main():
    port = '8181'
    auth = {'user': 'admin', 'password': 'admin'}
    args = docopt(__doc__, options_first=True)
    # args = {'--address': None, '--debug': False, '--help': False, '<args>': ['mount'], '<command>': 'node'}
    if args.get('--address') is not None:
        ctl = Session(args['--address'], port, auth.get('user', 'admin'), auth.get('password', 'admin'))
    else:
        ctl = Session('127.0.0.1', port, auth.get('user', 'admin'), auth.get('password', 'admin'))

    cmd = args['<command>']
    subcmd = args['<args>']
    commands = [cmd] + subcmd

    module = getattr(bvcctl, cmd)

    arguments = docopt(module.__doc__, commands)
    try:
        pass
        getattr(module, cmd)(ctl, arguments)
    except Exception, e:
        raise e

if __name__ == '__main__':
        main()
