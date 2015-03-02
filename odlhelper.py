#!/usr/bin/python
"""
Usage:
        odl get-nodes [--address]
        odl get-flows [--address]

Options :
    -A, --address           Address to bind UI
    -I, --ignore
    -h, --help
"""
import requests
from lib.docopt import docopt
import pprint
from requests.auth import HTTPBasicAuth


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'A': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'B': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'C': 'http://{server}:8181/restconf/operational/opendaylight-inventory:'}


class Controller(object):
    def __init__(self, restconf_server='localhost', port=8181):
        self.server = restconf_server
        self.port = port
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}
        self.auth = HTTPBasicAuth('admin', 'admin')

    def get_nodes(self):
        # try:
            resource = RESTAPI['NODEINVENTORY'].format(server=self.server)
            retval = self.session.get(resource, auth=self.auth, headers=self.headers)
            if retval.status_code == 200:
                data = retval.json()

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
        ctl.get_nodes()




