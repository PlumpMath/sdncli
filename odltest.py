import unittest
import requests
import sets
from requests.auth import HTTPBasicAuth
import pprint
from prettytable import PrettyTable


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
           'B': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'C': 'http://{server}:8181/restconf/operational/opendaylight-inventory:'}


# class TestODL(unittest.TestCase):
#     def test_request(self):
#         nodes = set()
#         server = "localhost"
#         session = requests.Session()
#         headers = {'content-type': 'application/xml'}
#         auth = HTTPBasicAuth('admin', 'admin')
#         # params = {'depth': '0'}
#         resource = RESTAPI['NODEINVENTORY'].format(server=server)
#         retval = session.get(resource, auth=auth, params=None, headers=headers)
#         self.assertTrue(retval.status_code, 200)
#         data = retval.json()
#         node_count = len(data["nodes"]["node"])
#         for i in range(node_count):
#             if "config" not in data["nodes"]["node"][i]["id"]:
#                 new_node = data["nodes"]["node"][i]["id"]
#                 nodes.add(new_node)
#         print nodes

# class TestJsonRequests(unittest.TestCase):
#     def test_request(self):
#         #Get List of Nodes
#         #Then use more specific scope iterator
#         nodes = set()
#         server = "localhost"
#         session = requests.Session()
#         auth = HTTPBasicAuth('admin', 'admin')
#         resource = RESTAPI['NODEINVENTORY'].format(server=server)
#         retval = session.get(resource, auth=auth, params=None, headers=None)
#         self.assertTrue(retval.status_code, 200)
#         data = retval.json()
#         nodes = data.get('nodes').get('node')
#         for i in nodes:
#             table = i.get("flow-node-inventory:table")
#             print("Table type: {}").format(type(table))
#             for flow in table:
#                 # print flow
#                 if flow is not None:
#                     s = flow.get('id')
#                     y = flow.get('match')
#                 # print(flow)
#                 # s = table.get("flow")
#                 # print("s type: {}").format(type(s))
#                 # for t in s:
#                 #     print t

#             # for x in n:
#             #     y = x.get("flow")
#             #     for z in y:
#             #         print y

#         # node_count = len(data["nodes"]["node"])
#         # for i in range(node_count):
#         #     if "config" not in data["nodes"]["node"][i]["id"]:
#         #         new_node = data["nodes"]["node"][i]["id"]
#         #         nodes.add(new_node)
#         # print nodes class TestJsonRequests(unittest.TestCase):

class TestGetFlows(unittest.TestCase):
    def test_request(self):
        #Get List of Nodes
        #Then use more specific scope iterator
        nodes = set()
        flowtable = {}
        server = "localhost"
        session = requests.Session()
        auth = HTTPBasicAuth('admin', 'admin')
        resource = RESTAPI['NODEINVENTORY'].format(server=server)
        try:
            retval = session.get(resource, auth=auth, params=None, headers=None)
        except Exception, e:
            raise e
    
        self.assertTrue(retval.status_code, 200)
        data = retval.json()
        nodes = data.get('nodes').get('node')
        for node in nodes:
            if "cont" not in node['id']:
                table = node['flow-node-inventory:table']
                for table_entry in table:
                    if 'flow' in table_entry:
                        #TODO check this list
                        flow_rule = table_entry.get('flow')[0]
                        flowmap = {'node': node['id'],
                                   'flow_id': flow_rule.get('id'),
                                   'table_id': flow_rule.get('table_id'),
                                   'hard_timeout': flow_rule.get('hard-timeout'),
                                   'idle_timeout': flow_rule.get('idle-timeout'),
                                   'match': flow_rule.get('match'),
                                   'instructions': flow_rule.get('instructions')
                                   }
                        flowtable.setdefault(flow_rule.get('cookie'), []).append(flowmap)

                        
                        
        pprint.pprint(flowtable)


class TestGetHosts(unittest.TestCase):
    def test_request(self):
        server = "localhost"
        hosttable = {}
        session = requests.Session()
        auth = HTTPBasicAuth('admin', 'admin')
        resource = RESTAPI['TOPOLOGY'].format(server=server)
        retval = session.get(resource, auth=auth, params=None, headers=None)
        self.assertTrue(retval.status_code, 200)
        data = retval.json()
        nodes = data.get('network-topology').get('topology')
        for node in nodes:
            topology_nodes = node.get('node')
            for t_node in topology_nodes:
                if 'host' in t_node.get('node-id'):
                    host = {'t_id': t_node.get('termination-point'),
                            'htsa': t_node.get('host-tracker-service:addresses')
                            }
                    hosttable.setdefault(t_node.get('node-id'), []).append(host)
       
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


class TestPrettyPrint(unittest.TestCase):
    def test_print(self):
        # Flow ID | Node | TableID |
        #   1     |   2  |    3    |
        #   4     |   5  |    6    |

        table = [{'Flow_id': 1, 'Node': 2, 'TableID': 3}, {'Flow_id': 4, 'Node': 5, 'TableID': 6}]
        header = table[0].keys()
        p = PrettyTable(header)
        p.padding_width = 1

        for i in table:
            p.add_row(i.values())
        print p


class TestDictPassing(unittest.TestCase):
    def test_pass(self):
        s = {'a':[{'foo':'bar', 'bar': 'baz'}, {'bar': 'foo', 'baz':'bar'}]}
        self.test_recv(s)

    def test_recv(self, s):
        self.assertIsInstance(d, dict)
        



if __name__ == '__main__':
    unittest.main(verbosity=3)
