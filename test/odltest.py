import unittest
import requests
import sys
import os
import uuid
from requests.auth import HTTPBasicAuth

import pprint

sys.path.insert(0, os.path.abspath(__file__+"/../.."))
from lib.bvclib import Controller

API = {'OPER': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
       'CONFIG': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes',
       'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
       'FLOWMOD': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
       'FLOW': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
       'MODULES': 'http://{server}:8181/restconf/modules',
       'MOUNTS': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/',
       'NETCONF': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/{resource}',
       'UNMOUNT': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{name}',
       }


class TestListExp(unittest.TestCase):
        ctl = Controller("localhost")
        moduletable = {}
        u = []
        # keys = {"netconf-node-inventory"}
        resource = API['MODULES'].format(server="localhost")
        headers = {'content-type': 'application/xml'}
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=headers)
        filter_keys = ('controller-config')
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            [moduletable.setdefault(str(uuid.uuid4()), [].append({'name': 'foo'})) for m in data['modules']['module']]
            pprint.pprint(moduletable)

# class TestGetHosts(unittest.TestCase):
#     def test_request(self):
#         server = "localhost"
#         hosttable = {}
#         session = requests.Session()
#         auth = HTTPBasicAuth('admin', 'admin')
#         resource = RESTAPI['TOPOLOGY'].format(server=server)
#         retval = session.get(resource, auth=auth, params=None, headers=None)
#         self.assertTrue(retval.status_code, 200)
#         data = retval.json()
#         nodes = data.get('network-topology').get('topology')
#         for node in nodes:
#             topology_nodes = node.get('node')
#             for t_node in topology_nodes:
#                 if 'host' in t_node.get('node-id'):
#                     host = {'t_id': t_node.get('termination-point'),
#                             'htsa': t_node.get('host-tracker-service:addresses')
#                             }
#                     hosttable.setdefault(t_node.get('node-id'), []).append(host)
       
        #     node_count = len(json_data["network-topology"]["topology"][0]["node"])
        #     if node_count > 0:

        #         for i in range(node_count):
        #             if 'host-tracker-service:id' in json_data['network-topology']['topology'][0]['node'][i]:
        #                 mytp = json_data['network-topology']['topology'][0]['node'][i]['termination-point']
        #                 myaddr = json_data['network-topology']['topology'][0]['node'][i]['host-tracker-service:addresses']
        #                 for l in mytp:
        #                     for k, v in l.items():
        #                         mac = v[5:22]
        #                         node_port = v[23:].split(':')
        #                         mapping = {'port': node_port[2],
        #                                    'switch': node_port[0] + ":" + node_port[1]}
        #                         self.hostmap.setdefault(mac, []).append(mapping)
        #                 for l in myaddr:
        #                         mapping = {'ip': l['ip']}
        #                         self.hostmap.setdefault(l['mac'], []).append(mapping)

        #         print self.hostmap
        #         #TODO Make Pretty
        #         for k, v in self.hostmap.items():
        #             print k, v
        # else:
        #     print "error"


# class TestPrettyPrint(unittest.TestCase):
#     def test_print(self):
#         # Flow ID | Node | TableID |
#         #   1     |   2  |    3    |
#         #   4     |   5  |    6    |

#         table = [{'Flow_id': 1, 'Node': 2, 'TableID': 3}, {'Flow_id': 4, 'Node': 5, 'TableID': 6}]
#         header = table[0].keys()
#         p = PrettyTable(header)
#         p.padding_width = 1

#         for i in table:
#             p.add_row(i.values())
#         print p


# class TestDictPassing(unittest.TestCase):
#     def test_pass(self):
#         s = {'a':[{'foo':'bar', 'bar': 'baz'}, {'bar': 'foo', 'baz':'bar'}]}
#         self.test_recv(s)

#     def test_recv(self, s):
#         self.assertIsInstance(d, dict)
        



if __name__ == '__main__':
    unittest.main(verbosity=3)
