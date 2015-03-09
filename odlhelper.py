#!/usr/bin/python
# (C)2015 Brocade Communications Systems, Inc.
# 130 Holger Way, San Jose, CA 95134.
# All rights reserved.
# Author: Gary Berger <gberger@brocade.com>
"""
Usage:
        odl get-nodes [--json]
        odl get-hosts [--json]
        odl get-flows [--json]
        odl delete-flow <node> <table> <flow>
        odl get-flow <node> <table> <flow>
        odl add-flow <node> <table> <flow>

Options :
    -A, --address           Address to bind UI
    -I, --ignore
    -h, --help
"""

import requests
from lib.docopt import docopt
from requests.auth import HTTPBasicAuth
import lib.bvctmpl as t
# from ncclient import manager
import pprint
from prettytable import PrettyTable


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
           'FLOWMOD': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
           'FLOW': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}'}


class Controller(object):
    def __init__(self, restconf_server='localhost', port=8181):
        self.port = port
        self.auth = HTTPBasicAuth('admin', 'admin')
        self.server = restconf_server
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}

    def get_nodes(self, dumpjson=False):
            nodetable = {}
        # try:
            resource = RESTAPI['NODEINVENTORY'].format(server=self.server)
            try:
                retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
            except Exception, e:
                raise e
            if retval.status_code == 200:
                data = retval.json()
                nodes = data.get('nodes').get('node')
                for node in sorted(nodes):
                    if "cont" not in node['id']:
                        nodeentry = {"Node": node.get('id')}
                        nodetable.setdefault(node.get('id'), []).append(nodeentry)
            self.print_table(nodetable)

    def get_flows(self, dumpjson=False):
        flowtable = self._get_flows()
        # for f in sorted(flowtable):
        #     print f

    def _get_flows(self, dumpjson=False):
        '''
        Get all flows known to controller. Traverses the node-inventory document to assemble.
        '''
        #TODO Better management of match and action types
        #TODO Should this be formatted similar to ovs-ofctl dumpflows
        # try:
        resource = RESTAPI['NODEINVENTORY'].format(server=self.server)
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
        except Exception, error:
            raise error

        if retval.status_code == 200:
            flowtable = {}
            data = retval.json()
            nodes = data.get('nodes').get('node')
            for node in nodes:
                if "cont" not in node['id']:
                    table = node['flow-node-inventory:table']
                    for table_entry in table:
                        if 'flow' in table_entry:
                            #TODO check the list depth
                            print table_entry
                            flow_rule = table_entry.get('flow')[0]
                            flowmap = {'node': node['id'],
                                       'match': flow_rule.get('match'),
                                       'flow_id': flow_rule.get('id'),
                                       'table_id': flow_rule.get('table_id'),
                                       'hard_timeout': flow_rule.get('hard-timeout'),
                                       'idle_timeout': flow_rule.get('idle-timeout'),
                                       'instructions': flow_rule.get('instructions')
                                       }
                            flowtable.setdefault(flow_rule.get('cookie'), []).append(flowmap)
            return flowtable
        else:
            print("Error with call {}").format(resource)
            print("Error: {}").format(resource.error)

    def get_hosts(self, dumpjson=False):
        dbhosts = {}
        hosttable = self._get_hosts()
        if hosttable is not None:
            for hosts in hosttable:
                host = hosttable.get(hosts)
                for h in host:
                    tid = h.get('t_id')
                    htsa = h.get('htsa')
                    for p in htsa:
                        for q in tid:
                            hostmap = {'IP': p.get('ip'), 'MacAddr': p.get('mac'), 'TID': q.get('tp-id')[23:]}
                            dbhosts.setdefault(p.get('id'), []).append(hostmap)
            self.print_table(dbhosts)
        else:
            print("Found no hosts")
            return

        # node_port = v[23:].split(':')
        #                         mapping = {'port': node_port[2],
        #                                    'switch': node_port[0] + ":" + node_port[1]}

    def _get_hosts(self, dumpjson=False):
        '''
        Get all hosts connected to known switches using topology data source
        '''
        resource = RESTAPI['TOPOLOGY'].format(server=self.server)
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
        except Exception, error:
            raise error

        if retval.status_code == 200:
            hosttable = {}
            data = retval.json()
            nodes = data.get('network-topology').get('topology')
            for node in nodes:
                topology_nodes = node.get('node')
                if topology_nodes is not None:
                    for t_node in topology_nodes:
                        if 'host' in t_node.get('node-id'):
                            host = {'t_id': t_node.get('termination-point'),
                                    'htsa': t_node.get('host-tracker-service:addresses')
                                    }
                            hosttable.setdefault(t_node.get('node-id'), []).append(host)
                else:
                    return None

        return hosttable

        #     for k, v in l.items():
        #         mac = v[5:22]
        #         node_port = v[23:].split(':')
        #         mapping = {'port': node_port[2],
        #                    'switch': node_port[0] + ":" + node_port[1]}

    def delete_flow(self, node, table, flow):
        resource = RESTAPI['DELETEFLOW'].format(server=self.server, node=node, table=table, flow=flow)
        retval = self.session.delete(resource, auth=self.auth, params=None, headers=self.headers)
        if retval.status_code is not "200":
            print retval.text

    def get_flow(self, node, table, flow):
        resource = RESTAPI['FLOW'].format(server=self.server, node=node, table=table, flow=flow)
        retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
        if retval.status_code is not "200":
            print retval.status_code
            print retval.text
        else:
            print retval.text

    def add_flow(self, node, table, flow, actions):
        print actions
        headers = {'content-type': 'application/xml'}
        resource = RESTAPI['FLOW'].format(server=self.server, node=node, table=table, flow=flow)
        retval = self.session.post(resource, auth=self.auth, params=None, headers=headers, data=actions)
        print resource
        print flow
        if retval.status_code is not "200":
            print retval.status_code
            print retval.text
        else:
            print retval.text

    # def netconf_connect(self, host, port, user):
    #     with manager.connect(host=host, port=830, username=user, hostkey_verify=False) as m:
    #         c = m.get_config(source='running').data_xml
    #     with open("%s.xml" % host, 'w') as f:
    #         f.write(c)

    def parse_hosttable(self, hosttable):
        for row in hosttable:
            print row

    def print_table(self, table):
        add_header = False
        for i in sorted(table):
            if not add_header:
                p = PrettyTable(table.get(i)[0].keys())
                p.padding_width = 1
                add_header = True
            p.add_row(table.get(i)[0].values())
        print p

if __name__ == "__main__":
    args = docopt(__doc__)
    ctl = Controller()
    if args["get-nodes"]:
        ctl.get_nodes(args["--json"])
    if args["get-hosts"]:
        ctl.get_hosts(args["--json"])
    if args["get-flows"]:
        pprint.pprint(ctl.get_flows(args["--json"]))
    if args["delete-flow"]:
        ctl.delete_flow(args['<node>'], args['<table>'], args['<flow>'])
    if args["get-flow"]:
        ctl.get_flow(args['<node>'], args['<table>'], args['<flow>'])
    if args["add-flow"]:
        ctl.add_flow(args['<node>'], args['<table>'], args['<flow>'], t.addflow)
