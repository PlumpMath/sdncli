
import requests
import pprint
import uuid
import json
import netconflib
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable

# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

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


class Controller(object):
    def __init__(self, restconf_server="localhost", username="admin", pw="admin",  port=8181):
        self.port = port
        self.auth = HTTPBasicAuth(username, pw)
        self.server = restconf_server or 'localhost'
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}

    def get_bvc_nodes(self, ds, dumpjson=False):
            #TODO fix key in output
            nodetable = {}
            filter_keys = ('controller-config')
            resource = API[ds].format(server=self.server)
            try:
                retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers, timeout=5)
            except requests.exceptions.ConnectionError:
                return(("Error connecting to BVC {}").format(self.server), False)
            if str(retval.status_code)[:1] == "2":
                data = retval.json()
                if dumpjson:
                    pprint.pprint(data)
                [nodetable.update({line['id']: ds.lower()}) for line in data['nodes']['node'] if line['id'] not in filter_keys]
            if len(nodetable) > 0:
                return (nodetable, True)
            else:
                return (("No Nodes Found").format(retval.status_code), False)

    def http_get(self, uri):
        try:
            retval = self.session.get(uri, auth=self.auth, params=None, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            try:
                data = retval.json()
            except ValueError:
                return("Bad JSON found", False)
            return(data, True)
        else:
            return (("Unknown Status Code").format(retval.status_code), False)

    def netconf_get(self, r, ds, payload, node):
        data = json.dumps(json.loads(payload))
        if node is None:
            node = "controller-config"
        resource = API['NETCONF'].format(server=self.server, resource=r, ds=ds, node=node)
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            return (("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            return (retval.json(), True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    def get_bvc_hosts(self, dumpjson=False):
        '''
        Get all hosts connected to known switches using topology data source
        '''
        resource = API['TOPOLOGY'].format(server=self.server)
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            hosttable = {}
            data = retval.json()
            if dumpjson:
                pprint.pprint(data)
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
                    return(hosttable, True)
                else:
                    return ("No hosts found", False)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    def get_modules(self, dumpjson=False):
        moduledb = {}
        resource = API['MODULES'].format(server=self.server)
        headers = {'content-type': 'application/xml'}
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=headers)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            if dumpjson:
                pprint.pprint(data)
            root = data['modules']['module']
            for line in root:
                modulemap = {'name':     line['name'],
                             'namespace': line['namespace'],
                             'revision':  line['revision']}
                moduledb.setdefault(str(uuid.uuid4()), []).append(modulemap)
            if len(moduledb) > 0:
                return(moduledb, True)
            else:
                return("No Modules found", False)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    def get_mounts(self, dumpjson=False):
        mountdb = {}
        (retval, status) = self._get_mount_status(dumpjson)
        mntstats = retval
        if status:
            keys = {"odl-sal-netconf-connector-cfg:sal-netconf-connector"}
            resource = API['MOUNTS'].format(server=self.server)
            headers = {'content-type': 'application/xml'}
            try:
                retval = self.session.get(resource, auth=self.auth, params=None, headers=headers)
            except requests.exceptions.ConnectionError:
                return(("Error connecting to BVC {}").format(self.server), False)
            if str(retval.status_code)[:1] == "2":
                data = retval.json()
                root = data['config:modules']['module']
                for line in root:
                    if line['type'] in keys:
                        mountmap = {'name':     line['name'],
                                    'address':  line['odl-sal-netconf-connector-cfg:address'],
                                    'port':     line['odl-sal-netconf-connector-cfg:port'],
                                    'username': line['odl-sal-netconf-connector-cfg:username'],
                                    'password': line['odl-sal-netconf-connector-cfg:password'],
                                    'connected':   mntstats[line['name']]
                                    }
                        mountdb.setdefault(str(uuid.uuid4()), []).append(mountmap)
                if len(mountdb) > 0:
                    return(mountdb, True)
                else:
                    return("No Mounts found", False)
            else:
                return (("Unexpected Status Code {}").format(retval.status_code), False)
        else:
                return (("{}").format(retval), False)

    def _get_mount_status(self, dumpjson=False):
        stats = {}
        # keys = {"netconf-node-inventory"}
        resource = API['OPER'].format(server=self.server)
        headers = {'content-type': 'application/xml'}
        try:
            retval = self.session.get(resource, auth=self.auth, params=None, headers=headers)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            root = data['nodes']['node']
            for line in root:
                if 'netconf-node-inventory:connected' not in line:
                    stats.update({line['id']: False})
                elif 'netconf-node-inventory:connected' in line:
                    stats.update({line['id']: line['netconf-node-inventory:connected']})
            return (stats, True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    def mount_netconf_device(self, name, node, user, pw, port, vdx=None):
        if not port:
            port = 830
        if vdx is not None:
            data = netconflib.netconf_mount_vdx(name, node, port, user, pw)
        else:
            data = netconflib.netconf_mount(name, node, port, user, pw)
        resource = API['MODULES'].format(server=self.server)
        headers = {'content-type': 'application/xml'}
        try:
            retval = self.session.post(resource, auth=self.auth, params=None, headers=headers, data=data)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(self.server), False)
        if str(retval.status_code)[:1] == "2":
            return(("Mounted Node {} on {}").format(name, node), True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    def unmount_netconf_device(self, name):
        resource = API['UNMOUNT'].format(server=self.server, name=name)
        headers = {'content-type': 'application/xml'}
        try:
            retval = self.session.delete(resource, auth=self.auth, params=None, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Error connecting to BVC {}").format(self.server)
            return None
        if str(retval.status_code)[:1] == "2":
            return(("UnMounted Node {}").format(name), True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)

    # def delete_flow(self, node, table, flow):
    #     resource = API['DELETEFLOW'].format(server=self.server, node=node, table=table, flow=flow)
    #     try:
    #         retval = self.session.delete(resource, auth=self.auth, params=None, headers=self.headers)
    #     except requests.exceptions.ConnectionError:
    #         return(("Error connecting to BVC {}").format(self.server), False)
    #     if str(retval.status_code)[:1] == "2":
    #         return(retval.text, True)
    #     else:
    #         return (("Unexpected Status Code {}").format(retval.status_code), False)

    # def get_flow(self, node, table, flow):
    #     resource = API['FLOW'].format(server=self.server, node=node, table=table, flow=flow)
    #     try:
    #         retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers)
    #     except requests.exceptions.ConnectionError:
    #         return(("Error connecting to BVC {}").format(self.server), False)
    #     if str(retval.status_code)[:1] == "2":
    #         return(retval.text, True)
    #     else:
    #         return (("Unexpected Status Code {}").format(retval.status_code), False)

    # def add_flow(self, node, table, flow, actions):
    #     print actions
    #     headers = {'content-type': 'application/xml'}
    #     try:
    #         resource = API['FLOW'].format(server=self.server, node=node, table=table, flow=flow)
    #     except requests.exceptions.ConnectionError:
    #         print("Error connecting to BVC {}").format(self.server)
    #         return None
    #     retval = self.session.post(resource, auth=self.auth, params=None, headers=headers, data=actions, timeout=5)
    #     if str(retval.status_code)[:1] == "2":
    #         return(retval.text, True)
    #     else:
    #         return (("Unexpected Status Code {}").format(retval.status_code), False)

    # def get_bvc_flow_entries(self, api, dumpjson):
    #     new_flow_entry = {}
    #     flowdb = {}
    #     resource = API[api].format(server=self.server)
    #     try:
    #         retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers, timeout=5)
    #     except requests.exceptions.ConnectionError:
    #         return(("Error connecting to BVC {}").format(self.server), False)
    #     if str(retval.status_code)[:1] == "2":
    #         data = retval.json()
    #         if dumpjson:
    #             pprint.pprint(data)
    #         nodes = data['nodes']['node']
    #         for node in nodes:
    #             if "cont" not in node.get('id'):
    #                 _nodeid = node.get('id')
    #                 if _nodeid is not None:
    #                     print "Nodeid: %s" % _nodeid
    #                     if "flow-node-inventory:table" in node:
    #                         table = node['flow-node-inventory:table']
    #                         for table_entry in table:
    #                             if 'flow' in table_entry:
    #                                 for flow_entry in table_entry.get('flow'):
    #                                     s = self.extract(flow_entry, new_flow_entry)
    #                                     flowmap = {'nodeid': _nodeid,
    #                                                # 'flowname': s['flow-name'],
    #                                                'hardtimeout': s['hard-timeout'],
    #                                                'idletimeout': s['idle-timeout'],
    #                                                'flowid': s['id'],
    #                                                'in_port': s['in-port'],
    #                                                'ipv4destination': s['ipv4-destination'],
    #                                                'order': s['order'],
    #                                                #TODO get index of nodes to dereference
    #                                                'outputnode': s['output-node-connector'],
    #                                                'priority': s['priority'],
    #                                                'table_id': s['table_id'],
    #                                                'ethertype': s['type']}
    #                                                 #'vlanid': s['vlan-id']}
    #                                                 #TODO  u'vlan-id-present': True}
    #                                     flowdb.setdefault(str(uuid.uuid4()), []).append(flowmap)
    #         return (flowdb, True)
    #     else:
    #         return (("Unexpected Status Code {}").format(retval.status_code), False)

    # def _get_flows1(self, dumpjson=False):
    #     #TODO Better management of match and action types
    #     #TODO Should this be formatted similar to ovs-ofctl dumpflows
    #     # try:
    #     resource = API['NODEINVENTORY'].format(server=self.server)
    #     try:
    #         retval = self.session.get(resource, auth=self.auth, params=None, headers=self.headers, timeout=5)
    #     except requests.exceptions.ConnectionError:
    #         print("Error connecting to BVC {}").format(self.server)
    #         return None

    #     if retval.status_code == 200:
    #         flowdb = {}
    #         data = retval.json()
    #         if dumpjson:
    #             pprint.pprint(data)
    #         nodes = data['nodes']['node']
    #         _flowid = None
    #         _priority = None
    #         _table_id = None
    #         _matchrule = None
    #         _cookie = None
    #         _outputorder = None
    #         _outputport = None
    #         _gototable = None
    #         for node in nodes:
    #             if "cont" not in node.get('id'):
    #                 _nodeid = node.get('id')
    #                 table = node['flow-node-inventory:table']
    #                 for table_entry in table:
    #                     if 'flow' in table_entry:
    #                         for flow_entry in table_entry.get('flow'):
    #                             pprint.pprint(flow_entry)
    #                             for ak, av in flow_entry.viewitems():
    #                                 # for k, v in (filter(lambda x: m in x, flow_entry.viewitems())):
    #                                 if 'table_id' in ak:
    #                                     _table_id = av
    #                                 if 'id' in ak:
    #                                     _flowid = av
    #                                 if 'cookie' in ak:
    #                                     _cookie = av
    #                                 if 'match' in ak:
    #                                     if isinstance(av, dict):
    #                                         for match in av.viewitems():
    #                                             _matchrule = match
    #                                     else:
    #                                         print "%s:%s" % (ak, av)
    #                                         _matchrule = "Unknown"
    #                                 if 'instructions' in ak:
    #                                     for b in av.get('instruction'):
    #                                         # _order = b.get('order')
    #                                         if 'go-to-table' in b:
    #                                             print("Found I")
    #                                             _gototable = b['go-to-table']
    #                                         else:
    #                                             for bk, bv in b.viewitems():
    #                                                 if isinstance(bv, dict):
    #                                                     for ck, cv in bv.viewitems():
    #                                                         if isinstance(cv, list):
    #                                                             for i in cv:
    #                                                                 _outputport = i['output-action']['output-node-connector']
    #                                                                 _outputorder = i['order']
    #                                                         elif isinstance(cv, dict):
    #                                                             for k,v in cv.viewitems():
    #                                                                 print("Key: {}, Value {}").format(ak, av)
    #                                                             print("Found Dict")
    #                                 if 'priority' in ak:
    #                                     _priority = av
    #                             flowmap = {'nodeid': _nodeid,
    #                                        'flowid': _flowid,
    #                                        'cookie': _cookie,
    #                                        'match': _matchrule,
    #                                        'output': _outputport,
    #                                        'goto': _gototable,
    #                                        'order': _outputorder,
    #                                        'table': _table_id,
    #                                        'priority': _priority}
    #                             flowdb.setdefault(str(uuid.uuid1()), []).append(flowmap)
    #                             _flowid = None
    #                             _priority = None
    #                             _table_id = None
    #                             _matchrule = None
    #                             _cookie = None
    #                             _outputorder = None
    #                             _outputport = None
    #                             _gototable = None
    #                             # else:
    #                             #     print("Unknown Key Found {}:{}").format(k, v)

    #                 return flowdb

    #     else:
    #         print("Error with call {}").format(resource)
    #         print("Error: {}").format(resource.error)
    #     return None

        #     for k, v in l.items():
        #         mac = v[5:22]
        #         node_port = v[23:].split(':')
        #         mapping = {'port': node_port[2],
        #                    'switch': node_port[0] + ":" + node_port[1]}

    # def _extract(self, ind, outd):
    #     for key, value in ind.viewitems():
    #         # print("Key: {key}, Value: {value}, Type: {type}").format(key=key, value=value, type=type(value))
    #         if isinstance(value, dict):
    #             self.extract(value, outd)
    #         elif isinstance(value, list):
    #             for i in value:
    #                 self.extract(i, outd)
    #         else:
    #             outd[key] = value
    #     return outd

    # def _extractkeys(self, ks, inputitems, outputitems):
    #     for key, value in inputitems.viewitems():
    #         # print("Key: {key}, Value: {value}, Type: {type}").format(key=key, value=value, type=type(value))
    #         if isinstance(value, dict):
    #             self.extractkeys(ks, value, outputitems)
    #         elif isinstance(value, list):
    #             for i in value:
    #                 if i['type'] in ks:
    #                     self.extractkeys(ks, i, outputitems)
    #         else:
    #             outputitems[key] = value
    #     return outputitems

    def print_table(self, text, table, sortkey=None):
        self.print_table_banner(text)
        self.print_table_detail(table, sortkey)

    def print_table_banner(self, text):
        print("+-------------------------+")
        print text

    def print_table_detail(self, table, sortkey=None):
        p = PrettyTable()
        p.field_names = table.get(table.keys()[0])[0].keys()
        p.sortby = sortkey
        p.padding_width = 1
        p.align = "l"
        for i in table:
            row = table.get(i)[0].values()
            p.add_row(row)
            # rows = [[row[sortindex]]+row for row in rows]
        #TODO Figure out how to put index column first and have secondary sort key.
        p.add_column('Index', range(len(table)))

        print p
        print("Total Records: {}").format(len(table))
