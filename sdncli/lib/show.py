"""
Usage:
        sdncli [options] show hosts
        sdncli [options] show mounts
        sdncli [options] show nodes
        sdncli [options] show flows <node> <table>
        sdncli [options] show flow <id>
        sdncli [options] show interfaces
        sdncli [options] show port-profile
        sdncli [options] show syslog

Options :
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore
            -d --debug             Debug

"""
from util import print_table_dict, remove_keys
from pybvc.common.status import STATUS
from pybvc.openflowdev.ofswitch import OFSwitch
from pybvc.common.utils import dict_unicode_to_string
# from pprint import pprint
from pybvc.netconfdev.vrouter.vrouter5600 import VRouter5600
from pybvc.netconfdev.vdx.nos import NOS
# from sdncli.lib.interface.interface import get_cliconf_devices
from sdncli.lib import interface
from sdncli.driver.mlx import MLX
from sdncli.driver.linux import Linux
import json


def show(ctl, args):
    # NODES
    if args.get('nodes'):
        table = []
        result = ctl.get_all_nodes_conn_status()
        for node in result.data:
            result = ctl.get_node_info(node.get('node'))
            if(result.status.eq(STATUS.OK)):
                d = result.data
                record = {'Node': node.get('node'),
                          'IPAddres': d.get('flow-node-inventory:ip-address'),
                          'SerialNo': d.get('flow-node-inventory:serial-number'),
                          'Software': d.get('flow-node-inventory:software'),
                          'Hardware': d.get('flow-node-inventory:hardware'),
                          'Connected': node.get('connected'),
                          'Description': d.get('flow-node-inventory:description'),
                          'Manufacturer': d.get('flow-node-inventory:manufacturer')}
                table.append(record)
        fields = ['Node', 'Connected', 'Description', 'Hardware',
                  'IPAddres', 'Manufacturer', 'SerialNo', 'Software']
        print_table_dict(fields, table)
        # print [[r['node'], r['connected'], node.clazz] for r in result.data for node in nodes if node.get_id() == r['node']]
    # HOSTS
    elif args.get('hosts'):
        if ctl.topology.get_hosts_cnt() > 0:
            table = []
            fields = ['IP', 'Mac', 'Id']
            hosts = ctl.topology.get_hosts()
            if hosts is not None:
                for host in hosts:
                    hostmap = {'Id': host.get_id(),
                               'Mac': host.get_mac_address(),
                               'IP': host.get_ip_address_for_mac(host.get_mac_address())}
                    table.append(dict(hostmap))
                print_table_dict(fields, table)
        else:
            print "No Hosts Found"
    # MOUNTS
    elif args.get('mounts'):
        result = ctl.build_netconf_config_objects()
        if(result.status.eq(STATUS.OK)):
            fields = ['name', 'port', 'address', 'username', 'password',
                      'connection_timeout_millis', 'connected']
            r_keys = ['keepalive_executor']
            table = []
            for i in result.data:
                result = ctl.check_node_conn_status(i.name)
                if(result.status.eq(STATUS.NODE_CONNECTED)):
                    i.connected = "True"
                else:
                    i.connected = "False"
                d = remove_keys(i.__dict__, r_keys)
                table.append(d)
            print_table_dict(fields, table)
        else:
            print "Houston we have a problem {}".format(result.get_status().to_string())

    # CONFIG
    elif args.get('config'):
        node = args.get('<node>')
        result = ctl.check_node_conn_status(node)
        if(result.status.eq(STATUS.NODE_CONNECTED)):
            result = ctl.get_node_config(node)
            if(result.status.eq(STATUS.OK)):
                print (result.data).json()
            else:
                print "Houston we have a problem"
        else:
                print "Node {} is not mounted".format(node)

    # TOPOLOGY
    elif args.get('topology'):
        print "show topology"
    # MODULES
    elif args.get('modules'):
        pass
        # result = ctl.get_config_modules()
    # STREAMS
    elif args.get('streams'):
        streams = ctl.get_streams_info().data
        # TODO This returns empty DICT
        if len(streams) > 0:
            print streams
        else:
            print "No streams found"
    # PROVIDERS
    elif args.get('providers'):
        pass
        # providers =  ctl.get_service_providers_info().data
        # if len(providers) > 0:
        #     for i in providers:
        #         print i
        # else:
        #     print "No providers found"
    # Port Profile
    elif args.get('port-profile'):
        table = []
        nodes = ctl.inventory.netconf_nodes
        if nodes is None:
            raise ("Can't obtain netconf device data")
            return
        for node in nodes:
            if 'NOS' in node.clazz:
                m = globals()[node.clazz](ctl, node.id, None, None, None, None, None)
                result = m.get_portprofile()
                if(result.status.eq(STATUS.OK)):
                    fields = ['Host', 'Profile', 'Macs']
                    tmp = json.loads(result.data).get('port-profile-global').get('port-profile')
                    for i in tmp:
                        record = {"Host": node.id,
                                  "Profile": i.get('name', None),
                                  "Macs": i.get('static', None),
                                  }
                        table.append(record)
        if table:
            print_table_dict(fields, table)
        else:
            return

    # Syslog
    elif args.get('syslog'):
        table = []
        nodes = ctl.inventory.netconf_nodes
        if nodes is None:
            raise ("Can't obtain netconf device data")
            return
        for node in nodes:
            if 'NOS' in node.clazz:
                m = globals()[node.clazz](ctl, node.id, None, None, None, None, None)
                result = m.get_syslog()
                if(result.status.eq(STATUS.OK)):
                    fields = ['Host', 'SyslogIP', 'VRF', 'Port']
                    if 'syslog-server' in result.data:
                        tmp = json.loads(result.data).get('logging').get('syslog-server')
                        for i in tmp:
                            record = {"Host": node.id,
                                      "SyslogIP": i.get('syslogip', None),
                                      "VRF": i.get('use-vrf', None),
                                      "Port": i.get('port', None),
                                      }
                            table.append(record)

        if table:
            print_table_dict(fields, table)
        else:
            return

    # FLOWS
    elif args.get('flows'):
        table = []
        node = args['<node>']
        flowtable = args.get('<table>', 0)
        ofswitch = OFSwitch(ctl, node)
        result = ofswitch.get_flows(flowtable, operational=True)
        if(result.status.eq(STATUS.OK)):
            fields = ['cookie', 'priority', 'id', 'match', 'action', 'packet-count', 'byte-count']
            for i in result.data:
                i['packet-count'] = dict_unicode_to_string(i.get('opendaylight-flow-statistics:flow-statistics').get('packet-count'))
                i['byte-count'] = dict_unicode_to_string(i.get('opendaylight-flow-statistics:flow-statistics').get('byte-count'))
                match = dict_unicode_to_string(i.get('match'))
                match = str(match).translate(None, '{\'\`\ }')
                i['match'] = str(match).replace(",", "\n")
                action = dict_unicode_to_string(i['instructions']['instruction'][0])
                action = str(action).translate(None, '\'\`\ []]')
                i['action'] = str(action).replace(",", "\n")
                table.append(i)
            print_table_dict(fields, table, 'id')
        else:
            print "No Flows Found"
    # INTERFACES
    # TODO break this up
    elif args.get('interfaces'):
        '''
        Get CLIConf devices
        '''
        int_table = []
        interfaces = interface.get_cliconf_devices(ctl)
        if interfaces is not None:
            if 'devices' in interfaces:
                devices = interfaces.get('devices').get('device')
                if devices is not None:
                    for device in devices:
                        name = device.get('name')
                        print "Grabbing interface for device {}".format(name)
                        filter = device.get("read-template-name")
                        if "mlx" in filter:
                            result = MLX.get_interfaces_cfg(ctl, name)
                            intf = MLX.maptoietfinterfaces(name, json.loads(result.data))
                            int_table = int_table + intf
                        elif ("linux" in filter):
                            result = Linux.get_interfaces_cfg(ctl, name)
                            intf = Linux.maptoietfinterfaces(name, json.loads(result.data))
                            int_table = int_table + intf
                        elif ("cisco" in filter):
                            result = Cisco.get_interfaces_cfg(ctl, name)
                            intf = Cisco.maptoietfinterfaces(name, json.loads(result.data))
                            int_table = int_table + intf

        result = ctl.build_netconf_config_objects()
        if(result.status.eq(STATUS.OK)):
            mounts = result.data
        else:
            raise ("Can't obtain mount data")
            return
        nodes = ctl.inventory.netconf_nodes
        if nodes is None:
            return

        for mount in mounts:
            for node in nodes:
                if 'controller-config' not in mount.name and mount.name == node.id:
                    name = node.id
                    port = mount.port
                    address = mount.address
                    user = mount.username
                    password = mount.password
                    clazz = node.clazz
                    print "Setting up connection for {} using driver {}".format(address, clazz)
                    # TODO This is wrong. I don't want to create an object to make this call..
                    m = globals()[clazz](ctl, name, address, port, user, password)
                    timeout = 60
                    result = m.get_interfaces_cfg(timeout)
                    if(result.status.eq(STATUS.OK)):
                        intf = m.maptoietfinterfaces(name, json.loads(result.data))
                        int_table = int_table + intf

        if int_table:
            fields = ['node', 'name', 'mtu', 'operstatus', 'adminstatus', 'ipv4-address', 'mac']
            print_table_dict(fields, int_table)
        else:
            return
