from uuid import uuid4
from utils import print_table

API = {'OPER': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
       'CONFIG': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes',
       'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
       'FLOWMOD': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
       'FLOW': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
       'MODULES': 'http://{server}:8181/restconf/modules',
       'UNMOUNTDEVICE': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{name}',
       'MOUNTDEVICE': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules',
       'MOUNTS': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/',
       'NETCONF': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount',
       'CAPABILITIES': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/ietf-netconf-monitoring:netconf-state',
       'GETSCHEMA': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/ietf-netconf-monitoring:get-schema'
       }

JMXAPI = {'HEAPUSAGE':  'http://{server}:8181/jolokia/read/java.lang:type=Memory/HeapMemoryUsage',
          'HEAPUSED': 'http://localhost:8181/jolokia/read/java.lang:type=Memory/HeapMemoryUsage/used',
          'GC':      'http://localhost:8181/jolokia/read/java.lang:type=GarbageCollector,*',
          'MEMORY': 'http://localhost:8181/jolokia/read/java.lang:type=Memory'}


def show_api(ctl):
    apitable = {}
    for k, v in API.viewitems():
        s = {'API': k, 'Link': v}
        apitable.setdefault(uuid4(), []).append(s)
    print_table("API", apitable)
