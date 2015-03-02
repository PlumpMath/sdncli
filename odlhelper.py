#!/usr/bin/python
"""
Usage:
        odl get-nodes [--json]
        odl get-hosts [--json]
        odl get-flows [--address]

Options :
    -A, --address           Address to bind UI
    -I, --ignore
    -h, --help
"""
import requests
from lib.docopt import docopt
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable
import json


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
           'B': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'C': 'http://{server}:8181/restconf/operational/opendaylight-inventory:'}


class Controller(object):
    def __init__(self, restconf_server='localhost', port=8181):
        self.server = restconf_server
        self.port = port
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}
        self.auth = HTTPBasicAuth('admin', 'admin')
        self.nodeset = set()
        #Can you have mac duplicated?
        self.hostmap = {}

    def print_table(self, columns, rows):
        table = PrettyTable()
        # table = PrettyTable(["Nodes"])
        # for i in columns - 1:
        #     table.add_row(i)
        print table

    def get_nodes(self, dumpjson=False):
        # try:
            resource = RESTAPI['NODEINVENTORY'].format(server=self.server)
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
            if retval.status_code == 200:
                data = retval.text
                json_data = json.loads(data)
                if dumpjson is not False:
                    print json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))
                node_count = len(json_data["nodes"]["node"])
                for i in range(node_count):
                    if "config" not in json_data["nodes"]["node"][i]["id"]:
                        new_node = json_data["nodes"]["node"][i]["id"]
                        self.nodeset.add(new_node)

                for i in sorted(self.nodeset):
                    print i
            # except Exception, e:

    def get_hosts(self, dumpjson=False):
        # try:
            resource = RESTAPI['TOPOLOGY'].format(server=self.server)
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
            if retval.status_code == 200:
                data = retval.text
                json_data = json.loads(data)
                if dumpjson is not False:
                    print json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))
                node_count = len(json_data["network-topology"]["topology"][0]["node"])
                # for i in range(node_count):
                #     if "host" in json_data["network-topology"]["topology"][0]["node"][i]["node-id"]:
                #         new_host = json_data["network-topology"]["topology"][0]["node"][i]["node-id"]
                #         self.hostmap[new_host[5:]] = ''
                for i in range(node_count):
                    if 'host-tracker-service:addresses' in json_data['network-topology']['topology'][0]['node'][i]:
                        mylist = json_data['network-topology']['topology'][0]['node'][i]['host-tracker-service:addresses']
                        for l in mylist:
                            mapping = {'ip': l['ip']}
                            self.hostmap.setdefault(l['mac'], []).append(mapping)

                for i in range(node_count):
                    if 'host-tracker-service:id' in json_data['network-topology']['topology'][0]['node'][i]:
                        mylist = json_data['network-topology']['topology'][0]['node'][i]['termination-point']
                        for l in mylist:
                            for k, v in l.items():
                                mac = v[5:22]
                                node_port = v[23:].split(':')
                                node = node_port[0] + ":" + node_port[1]
                                mapping = {'port': node_port[2],
                                           'switch': node_port[0] + ":" + node_port[1]}
                                self.hostmap.setdefault(mac, []).append(mapping)

                for k, v in self.hostmap.items():
                    print "{0}    {1}    {2}    {3}".format(k, v[0]['ip'], v[1]['switch'], v[1]['port'])
            else:
                print "error"
        # except Exception, e:
        #     raise e

    def get_flows(self):
        pass

    def set_flow(self, src, dst, ):

        # PUT http://192.168.239.129:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/1

        # APIDICT = {"Table": "http://{host}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}:{port}/flow-node-inventory:table/{table_num}/flow/{flow_num}"}

        '''

        # content-type: application/yang.data+json


        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <flow xmlns="urn:opendaylight:flow:inventory">
            <strict>false</strict>
            <table_id>0</table_id>
            <id>1</id>
            <priority>5</priority>
            <hard-timeout>0</hard-timeout>
            <idle-timeout>0</idle-timeout>
            <installHw>true</installHw>
            <flow-name>DropAll</flow-name>
            <instructions>
                <instruction>
                    <order>0</order>
                    <apply-actions>
                        <action>
                            <order>0</order>
                            <drop-action/>
                        </action>
                    </apply-actions>
                </instruction>
            </instructions>
        </flow>
        '''


if __name__ == "__main__":
    args = docopt(__doc__)
    ctl = Controller()
    if args["get-nodes"]:
        ctl.get_nodes(args["--json"])
    if args["get-hosts"]:
        ctl.get_hosts(args["--json"])




