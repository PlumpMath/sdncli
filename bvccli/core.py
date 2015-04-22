#!/usr/bin/python
# (C)2015 Brocade Communications Systems, Inc.
# 130 Holger Way, San Jose, CA 95134.
# All rights reserved.
# Author: Gary Berger <gberger@brocade.com>
"""
Brocade Vyatta Controller - Command Line Interface
Brocade Communications, Inc.

Usage:
        bvccli [options] <command> [<args>...]

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen

Commands:
             api           Print out existing HTTP APIs supported
             flows         Retrieve all known flows from the controller
             hosts         Retroeve all known hosts from the controller
             modules       Retrieve controller modules 
             nodes         Retrieve all known nodes from the controller
             netconf       Perform NetConf related functions such as retrieve configuration
             http          Perform HTTP based operations
             system        Perform queries on the BVC system itself

"""


import docopt


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
    from common import utils
    args = docopt.docopt(__doc__,  version="0.9.0", options_first=True)
    auth = utils.load_json_config()
    argv = [args['<command>']] + args['<args>']
    ctl = Controller(auth, args['--address'])
    if args['<command>'] == 'nodes':
        from common import nodes
        nodes.show_nodes(ctl, args)
    elif args['<command>'] == 'hosts':
        from common import hosts
        hosts.show_hosts(ctl, args)
    elif args['<command>'] == 'modules':
        from common import modules
        modules.show_modules(ctl, args)
    elif args['<command>'] == 'api':
        from common import api
        api.show_api(ctl)
    elif args['<command>'] == 'flows':
        print "Not implemented yet"
    elif args['<command>'] == 'http-get':
        from common import utils
        utils.http_get(args['uri'])
    elif args['<command>'] == 'netconf':
        from netconf import bvc_netconf
        from netconf import netconf
        from netconf import mounts
        netconf_args = bvc_netconf.docopt(bvc_netconf.__doc__, argv=argv)
        if(netconf_args['schema']):
            netconf.show_schema(ctl, netconf_args)
        elif(netconf_args['schemas']):
            netconf.get_schemas(ctl, netconf_args)
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
    elif args['<command>'] == 'http':
        from httplib import bvc_http
        from httplib import httplib
        http_args = bvc_http.docopt(bvc_http.__doc__, argv=argv)
        if(http_args['get']):
            httplib.http_get(ctl, http_args)
    elif args['<command>'] == 'system':
        from system import bvc_system
        from system import system
        system_args = bvc_system.docopt(bvc_system.__doc__, argv=argv)
        if(system_args['heap']):
            system.system_get_heapinfo(ctl, system_args)
        elif(system_args['gc']):
            system.system_get_gcinfo(ctl, system_args)
