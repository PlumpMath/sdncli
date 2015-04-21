#!/usr/bin/python
# (C)2015 Brocade Communications Systems, Inc.
# 130 Holger Way, San Jose, CA 95134.
# All rights reserved.
# Author: Gary Berger <gberger@brocade.com>
"""
Usage:
        bvccli [options] <command> [<args>...]

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen

Commands:
             api
             flows
             hosts
             modules
             nodes
             netconf       Perform NetConf related functions such as retrieve configuration
             http-get

"""


import docopt
from common import utils

import requests
from requests.auth import HTTPBasicAuth


# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class Controller(object):
    def __init__(self, auth, address):
        self.port = auth.get('port', 8181)
        self.auth = HTTPBasicAuth(auth.get('username', 'admin'), auth.get('password', 'admin'))
        self.server = address or auth.get('server')
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}


def main():
    args = docopt.docopt(__doc__,  version="0.9.0", options_first=True)
    auth = utils.load_json_config()
    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'nodes':
        from common import nodes
        ctl = Controller(auth, args['--address'])
        nodes.show_nodes(ctl, debug=False)
    elif args['<command>'] == 'hosts':
        from common import hosts
        ctl = Controller(auth, args['--address'])
        hosts.show_hosts(ctl, debug=False)
    elif args['<command>'] == 'modules':
        from common import modules
        ctl = Controller(auth, args['--address'])
        modules.show_modules(ctl, debug=False)
    elif args['<command>'] == 'api':
        from common import api
        ctl = Controller(auth, args['--address'])
        api.show_api(ctl)
    elif args['<command>'] == 'netconf':
        from netconf import bvc_netconf
        from netconf import netconf
        from netconf import mounts
        ctl = Controller(auth, args['--address'])
        netconf_args = bvc_netconf.docopt(bvc_netconf.__doc__, argv=argv)
        if(netconf_args['schema']):
            netconf.show_schema(ctl, netconf_args)
        elif(netconf_args['schemas']):
            netconf.show_schemas(ctl, netconf_args)
        elif(netconf_args['config']):
            netconf.show_config(ctl, netconf_args)
        elif(netconf_args['capabilities']):
            netconf.show_capabilities(ctl, netconf_args)
        elif(netconf_args['mount']):
            mounts.mount_device(ctl, netconf_args)
        elif(netconf_args['unmount']):
            mounts.unmount_device(ctl, netconf_args)
        elif(netconf_args['mounts']):
            mounts.show_mounts(ctl, netconf_args)


