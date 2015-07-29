from uuid import uuid4
from utils import print_table
# from ..httplib import httplib


API = {'BASE': 'http://{server}:8181/restconf/{resource}',
       'OPER': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes',
       'CONFIG': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes',
       'TOPOLOGY': 'http://{server}:8181/restconf/operational/network-topology:network-topology/',
       'FLOW':    'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}/flow/{flow}',
       'FLOWS': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes/node/{node}/flow-node-inventory:table/{table}',
       'MODULES': 'http://{server}:8181/restconf/modules',
       'UNMOUNTDEVICE': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{name}',
       'MOUNTDEVICE': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules',
       'MOUNTS': 'http://{server}:8181/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/',
       'NETCONF': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount{resource}',
       'CAPABILITIES': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/ietf-netconf-monitoring:netconf-state',
       'GETSCHEMA': 'http://{server}:8181/restconf/{ds}/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/ietf-netconf-monitoring:get-schema',
       'CTLAPIS': 'http://{server}:8181/apidoc/apis',
       'OPERATIONS': 'http://{server}:8181/restconf/operations/opendaylight-inventory:nodes/node/{node}/yang-ext:mount',
       'NOSINTERFACE': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/brocade-interface:interface',
       'VRINTERFACE': 'http://{server}:8181/restconf/operational/opendaylight-inventory:nodes/node/{node}/yang-ext:mount/vyatta-interfaces:interfaces',
       'STREAM': ' http://{server}:8181/restconf/operations/sal-remote:create-data-change-event-subscription'
       }

JMXAPI = {'HEAPUSAGE':  'http://{server}:8181/jolokia/read/java.lang:type=Memory/HeapMemoryUsage',
          'HEAPUSED': 'http://{server}:8181/jolokia/read/java.lang:type=Memory/HeapMemoryUsage/used',
          'GC':      'http://{server}:8181/jolokia/read/java.lang:type=GarbageCollector,*',
          'NONHEAP': 'http://{server}:8181/jolokia/read/java.lang:type=Memory/NonHeapMemoryUsage'}



