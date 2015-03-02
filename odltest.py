import unittest
import requests
import yaml
import json
import pprint
from requests.auth import HTTPBasicAuth


RESTAPI = {'NODEINVENTORY': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
           'A': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'B': 'http://{server}:8181/restconf/operational/opendaylight-inventory:',
           'C': 'http://{server}:8181/restconf/operational/opendaylight-inventory:'}


class TestODL(unittest.TestCase):
    def test_request(self):
        server = "localhost"
        session = requests.Session()
        headers = {'content-type': 'application/xml'}
        auth = HTTPBasicAuth('admin', 'admin')
        # params = {'depth': '0'}
        resource = RESTAPI['NODEINVENTORY'].format(server=server)
        retval = session.get(resource, auth=auth, params=None, headers=headers)
        data = retval.json()
        print data
        print "\n### Return ####\n"
        for k1, v1 in data.items():
            print k1, v1
        # for key in data['nodes']:
        #     if data["nodes"]["node"][0]['flow-node-inventory:description']:
        #         print "yes"
        #     #
        #     # s = data["nodes"]["node"][0]["id"]
        #     # # print data["nodes"]["node"][1]["id"]
        #     # print data["nodes"]["node"][2]["id"]
        #     # print data["nodes"]["node"][3]["id"]
        #     # print data["nodes"]["node"][4]["id"]

        self.assertTrue(retval.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)
