import unittest
import requests
import sets
from requests.auth import HTTPBasicAuth


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'A': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'B': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'C': 'http://{server}:8181/restconf/operational/opendaylight-inventory:'}


class TestODL(unittest.TestCase):
    def test_request(self):
        nodes = set()
        server = "localhost"
        session = requests.Session()
        headers = {'content-type': 'application/xml'}
        auth = HTTPBasicAuth('admin', 'admin')
        # params = {'depth': '0'}
        resource = RESTAPI['NODEINVENTORY'].format(server=server)
        retval = session.get(resource, auth=auth, params=None, headers=headers)
        self.assertTrue(retval.status_code, 200)
        data = retval.json()
        node_count = len(data["nodes"]["node"])
        for i in range(node_count):
            if "config" not in data["nodes"]["node"][i]["id"]:
                new_node = data["nodes"]["node"][i]["id"]
                nodes.add(new_node)
        print nodes 

if __name__ == '__main__':
    unittest.main(verbosity=2)
