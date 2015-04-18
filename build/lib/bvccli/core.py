#!/usr/bin/python
# (C)2015 Brocade Communications Systems, Inc.
# 130 Holger Way, San Jose, CA 95134.
# All rights reserved.
# Author: Gary Berger <gberger@brocade.com>
"""
Usage:
        bvccli  api              [options]
        bvccli  capabilities     [options] <node>
        bvccli  config           [options] <node> (--ops | --config)
        bvccli  flows            [options]
        bvccli  hosts            [options]
        bvccli  modules          [options]
        bvccli  mounts           [options]
        bvccli  nodes            [options]
        bvccli  schema           [options] <node> <module>
        bvccli  mount            [options] <name> <address> <user> <password> [--port <port>] [--mlx]
        bvccli  unmount          [options] <name>
        bvccli  http-get         [options] <uri>
        bvccli  get-allschemas   [options] <node>
        bvccli  post-netconf     [options] <resource> [--node <node>] (--ops | --config) [--payload <json>]

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen
"""


import docopt
from bvclib import Controller
from bvclib import API
import uuid
import pprint
import utils


class BvcCLI(object):
    def __init__(self, ctx):
        self.ctl = ctx

    def show_api(self):
        apitable = {}
        for k, v in API.viewitems():
            s = {'API': k, 'Link': v}
            apitable.setdefault(uuid.uuid4(), []).append(s)
        utils.print_table("API", apitable)

    def show_nodes(self, args):
        debug = (args["--debug"])
        nodemap = {}
        nodetable = {}

        (retval, status) = self.ctl.get_bvc_nodes('OPER', debug)
        if status:
            node_ops = retval
            (retval, status) = self.ctl.get_bvc_nodes('CONFIG', debug)
            if status:
                node_config = retval
                nodemap = node_ops.copy()
                nodemap.update(node_config)
            else:
                nodemap = node_ops

            for n in nodemap:
                s = {'node': n, 'status': nodemap[n]}
                nodetable.setdefault(uuid.uuid4(), []).append(s)
            utils.print_table("get_nodes", nodetable)
        else:
            print("Error: {}").format(retval)

    def show_hosts(self, args):
        debug = (args["--debug"])
        dbhosts = {}
        (retval, status) = self.ctl.get_bvc_hosts(debug)
        hosttable = retval
        if status:
            #TODO Check empty collection
            if hosttable is not None:
                for hosts in hosttable:
                    host = hosttable.get(hosts)
                    for h in host:
                        tid = h.get('t_id')
                        htsa = h.get('htsa')
                        for p in htsa:
                            for q in tid:
                                hostmap = {'IP': p.get('ip'), 'MacAddr': p.get('mac'), 'TID': q.get('tp-id')}
                                dbhosts.setdefault(p.get('id'), []).append(hostmap)
                if len(dbhosts) > 0:
                    utils.print_table("get_hosts", dbhosts)
                else:
                    print "Found no Hosts"
                    return
            #TODO ?
            else:
                print "No hosts found"
                return None
        else:
            print("Error: {}").format(retval)

        # node_port = v[23:].split(':')
        #                         mapping = {'port': node_port[2],
        #                                    'switch': node_port[0] + ":" + node_port[1]}

    # def show_flows(args):
    #     debug = args["--debug"]
    #     (configtable, status) = self.ctl.get_bvc_flow_entries("NODECONFIG", debug)
    #     if status:
    #         if configtable is not None and len(configtable) > 0:
    #                 self.print_table("get_flows", configtable, 'nodeid')
    #         else:
    #             print "No flows found in configuration table"
    #             return None
    #         opstable = self.get_bvc_flow_entries("NODECONFIG", debug)
    #         if configtable is not None and len(configtable) > 0:
    #                 self.print_table("get_flows", configtable, 'nodeid')
    #         else:
    #             print "No flows found in configuration table"
    #             return False

    def show_modules(self, args):
        print args
        debug = (args["--debug"])
        (retval, status) = self.ctl.get_modules(debug)
        if status:
            utils.print_table("show-modules", retval, 'name')
        else:
            print("Houston we have a problem, {}").format(retval)

    def get_capabilities(self, args):
        debug = (args["--debug"])
        (retval, status) = self.ctl.get_capabilities(args["<node>"], debug)
        if status:
            utils.print_table("Node Capabilities", retval, 'namespace')
        else:
            print("Houston we have a problem, {}").format(retval)

    def get_schema(self, args):
        module = args['<module>']
        node = args['<node>']
        data = {'input': {'identifier': module}}
        (retval, status) = self.ctl.netconf_get_schema(node, data)
        if status:
            print retval.json()['get-schema']['output']['data']

    def get_all_schemas(self, args):
        node = args['<node>']
        (retval, status) = self.ctl.get_capabilities(node)
        if status:
            for i in retval.iteritems():
                data = {'input': {'identifier': i[1][0]['namespace'].rsplit(':', 1)[1]}}
                (retval, status) = self.ctl.netconf_get_schema(node, data)
                if status:
                    print retval.json()['get-schema']['output']['data']

    def show_mounts(self, args):
        debug = (args["--debug"])
        (retval, status) = self.ctl.get_mounts(debug)
        if status:
            utils.print_table("mounts", retval, 'name')
        else:
            print("Houston we have a problem, {}").format(retval)

    def http_get(self, args):
        uri = args['<uri>']
        (retval, status) = self.ctl.http_get(uri)
        if status:
            print retval
        else:
            print("Houston we have a problem, {}").format(retval)

    def get_config(self, args):
        if(args['--ops']):
            ds = 'operational'
        else:
            ds = 'config'
        (retval, status) = self.ctl.netconf_get(args["<node>"], ds, 'NETCONF')
        if status:
            pprint.pprint(retval)
        else:
            print("Houston we have a problem, {}").format(retval)

    def post_netconf(self, args):
        if(args['--ops']):
            ds = 'operational'
        else:
            ds = 'config'
        (retval, status) = self.ctl.netconf_post(args["<resource>"], ds, args['<json>'], args["<node>"])
        if status:
            pprint.pprint(retval)
        else:
            print("Houston we have a problem, {}").format(retval)

    def mount_device(self, args):
        (retval, status) = self.ctl.mount_netconf_device(args['<name>'], args['<address>'], args['<user>'], args['<password>'], args['<port>'], args['--mlx'])
        if status:
            print(retval)
        else:
            print("Houston we have a problem, {}").format(retval)

    def unmount_device(self, args):
        (retval, status) = self.ctl.unmount_netconf_device(args['<name>'])
        if status:
            print(retval)
        else:
            print("Houston we have a problem, {}").format(retval)

    def parse_hosttable(self, hosttable):
        for row in hosttable:
            print row


def main():
    args = docopt.docopt(__doc__)
    auth = utils.load_json_config()
    ctl = Controller(auth, args['--address'])
    cli = BvcCLI(ctl)

    if args["nodes"]:
        cli.show_nodes(args)
    if args["hosts"]:
        cli.show_hosts(args)
    if args["flows"]:
        print "Not Implemented"
    if args["modules"]:
        cli.show_modules(args)
    if args["mounts"]:
        cli.show_mounts(args)
    if args["api"]:
        cli.show_api()
    if args['http-get']:
        cli.http_get(args)
    if args['config']:
        cli.get_config(args)
    if args['schema']:
        cli.get_schema(args)
    if args['capabilities']:
        cli.get_capabilities(args)
    if args['post-netconf']:
        cli.post_netconf(args)
    if args['get-allschemas']:
        cli.get_all_schemas(args)
    # # if args["del-flow"]:
    # #     self.ctl.delete_flow(args['<node>'], args['<table>'], args['<flow>'])
    # # if args["get-flow"]:
    # #     self.ctl.get_flow(args['<node>'], args['<table>'], args['<flow>'])
    # # if args["add-flow"]:
    # #     self.ctl.add_flow(args['<node>'], args['<table>'], args['<flow>'])
    if args["mount"]:
        cli.mount_device(args)
    if args["unmount"]:
        cli.unmount_device(args)
