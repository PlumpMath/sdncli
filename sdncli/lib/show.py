# [SublimeLinter flake8-ignore:-E302,+W601 flake8-max-line-length:120]
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
import json
import importlib

from pysdn.common.status import STATUS
from pysdn.openflowdev.ofswitch import OFSwitch
from pysdn.common.utils import dict_unicode_to_string
import pysdn.netconfdev as netconfdev
from pysdn.netconfdev.vrouter.vrouter5600 import VRouter5600  # noqa
from pysdn.netconfdev.vdx.nos import NOS  # noqa


from util import print_table_dict, remove_keys, isconnected


def show(ctl, args):
    # NODES
    if args.get('nodes'):
        table = []
        result = ctl.get_all_nodes_conn_status()
        for node in result.data:
            result = ctl.get_node_info(node.get('node'))
            if(result.status.eq(STATUS.OK)):
                retval = result.data
                record = {'Node': node.get('node'),
                          'IPAddress': retval.get('flow-node-inventory:ip-address'),
                          'SerialNo': retval.get('flow-node-inventory:serial-number'),
                          'Software': retval.get('flow-node-inventory:software'),
                          'Hardware': retval.get('flow-node-inventory:hardware'),
                          'Connected': node.get('connected'),
                          'Description': retval.get('flow-node-inventory:description'),
                          'Manufacturer': retval.get('flow-node-inventory:manufacturer')}
                table.append(record)
        fields = ['Node', 'Connected', 'Description', 'Hardware',
                  'IPAddress', 'Manufacturer', 'SerialNo', 'Software']
        print_table_dict(fields, table)
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
            for retval in result.data:
                result = ctl.check_node_conn_status(retval.name)
                if(result.status.eq(STATUS.NODE_CONNECTED)):
                    retval.connected = "True"
                else:
                    retval.connected = "False"
                rem_keys = remove_keys(retval.__dict__, r_keys)
                table.append(rem_keys)
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
    # Port Profile
    elif args.get('port-profile'):
        table = []
        nodes = ctl.inventory.netconf_nodes
        if nodes is None:
            raise ("Can't obtain netconf device data")
            return
        for node in nodes:
            if 'NOS' in node.clazz:
                module = globals()[netconfdev.node.clazz](ctl, node.id, None, None, None, None, None)
                result = module.get_portprofile()
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
                module = globals()[node.clazz](ctl, node.id, None, None, None, None, None)
                result = module.get_syslog()
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
            fields = ['cookie', 'priority', 'id', 'match',
                      'action', 'packet-count', 'byte-count']
            for retval in result.data:
                retval['packet-count'] = dict_unicode_to_string(retval.get('opendaylight-flow-statistics:flow-statistics').get('packet-count'))
                retval['byte-count'] = dict_unicode_to_string(retval.get('opendaylight-flow-statistics:flow-statistics').get('byte-count'))
                match = dict_unicode_to_string(retval.get('match'))
                match = str(match).translate(None, '{\'\`\ }')
                retval['match'] = str(match).replace(",", "\n")
                action = dict_unicode_to_string(retval['instructions']['instruction'][0])
                action = str(action).translate(None, '\'\`\ []]')
                retval['action'] = str(action).replace(",", "\n")
                table.append(retval)
            print_table_dict(fields, table, 'id')
        else:
            print "No Flows Found"
    # INTERFACES
    # TODO break this up
    elif args.get('interfaces'):
        '''
        Get CLIConf devices
        '''
        modulename = "sdncli.lib.interfaces"
        module = importlib.import_module(modulename, package=None)
        int_table = []
        interfaces = module.get_cliconf_devices(ctl)
        if interfaces is not None:
            if 'devices' in interfaces:
                devices = interfaces.get('devices').get('device')
                if devices is not None:
                    for device in devices:
                        name = device.get('name')
                        print "Grabbing interface for device {}".format(name)
                        filter = device.get("read-template-name")
                        if "mlx" in filter:
                            module = importlib.import_module("sdncli.driver.mlx", package=None)
                            result = module.MLX.get_interfaces_cfg(ctl, name)
                            intf = module.MLX.maptoietfinterfaces(name, json.loads(result.data))
                            int_table = int_table + intf
                        elif ("linux" in filter):
                            module = importlib.import_module("sdncli.driver.linux", package=None)
                            result = module.Linux.get_interfaces_cfg(ctl, name)
                            intf = module.Linux.maptoietfinterfaces(name, json.loads(result.data))
                            int_table = int_table + intf
                        elif ("cisco" in filter):
                            module = importlib.import_module("sdncli.driver.cisco", package=None)
                            result = module.Cisco.get_interfaces_cfg(ctl, name)
                            intf = module.Cisco.maptoietfinterfaces(name, json.loads(result.data))
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
                if 'controller-config' not in mount.name and mount.name == node.id and isconnected(ctl, node.id):
                    name = node.id
                    port = mount.port
                    address = mount.address
                    user = mount.username
                    password = mount.password
                    clazz = node.clazz
                    print "Setting up connection for {} using driver {}".format(address, clazz)
                    # TODO This is wrong. I don't want to create an object to make this call..
                    # change to staticmethods
                    m = globals()[clazz](ctl, name, address, port, user, password)
                    # timeout = 60
                    #TODO fix pysdn to add timeout..
                    result = m.get_interfaces_cfg()
                    if(result.status.eq(STATUS.OK)):
                        intf = m.maptoietfinterfaces(name, json.loads(result.data))
                        int_table = int_table + intf
        if int_table:
            fields = ['node', 'name', 'mtu', 'operstatus', 'adminstatus', 'ipv4-address', 'mac']
            print_table_dict(fields, int_table)
        else:
            print("No available targets found")
