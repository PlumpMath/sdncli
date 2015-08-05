"""
Usage:
        bvcctl show hosts
        bvcctl show mounts
        bvcctl show nodes
        bvcctl show flows <node> <table>
        bvcctl show flow <id> 
        bvcctl show interfaces
        bvcctl show modules
        bvcctl show rpc <node>
        bvcctl show streams
        bvcctl show providers
        bvcctl show inventory

Options :
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""
from common.api import API
from util import print_table_dict
from pybvc.common.status import STATUS
from pybvc.openflowdev.ofswitch import OFSwitch
from pybvc.openflowdev.ofswitch import Match
from pybvc.common.utils import dict_unicode_to_string


# from pybvc.controller.topology import Topology


def show(ctl, args):
    # NODES
    if args.get('nodes'):
        result = ctl.get_all_nodes_conn_status()
        fields = ['node', 'connected']
        print_table_dict(fields, result.data)
    # HOSTS
    elif args.get('hosts'):
        if ctl.topology.get_hosts_cnt() > 0:
            table = []
            hosts = ctl.topology.get_hosts()
            print hosts
            if hosts is not None:
                for host in hosts:
                    nodemap = {'Id': host.get_id(),
                               'Mac': host.get_mac_address(),
                               'IP': host.get_ip_address_for_mac(host.get_mac_address())}
                    table.append(dict(nodemap))
                print_table_dict('Modules', table)
        else:
            print "No Hosts Found"
    # MOUNTS
    elif args.get('mounts'):
        result = ctl.build_netconf_config_objects()
        fields = ['name', 'port', 'address', 'username', 'password', 'connection_timeout_millis']
        table = []
        for i in result.data:
            table.append(i.__dict__)
        print_table_dict(fields, table)

    # TOPOLOGY
    elif args.get('topology'):
        print "show topology"
    # MODULES
    elif args.get('modules'):
        pass
        # result = ctl.get_config_modules()
    elif args.get('streams'):
        print ctl.get_streams_info().data
    elif args.get('providers'):
        print ctl.get_service_providers_info().data
    elif args.get('flows'):
        table = []
        node = args['<node>']
        flowtable = args.get('<table>', 0)
        ofswitch = OFSwitch(ctl, node)
        result = ofswitch.get_flows(flowtable, operational=True)
        fields = ['cookie', 'priority', 'id', 'match', 'action']
        for i in result.data:
            match = dict_unicode_to_string(i.get('match'))
            match = str(match).translate(None, '{\'\`\ }')
            i['match'] = str(match).replace(",", "\n")
            action = dict_unicode_to_string(i['instructions']['instruction'][0])
            action = str(action).translate(None, '\'\`\ []]')
            i['action'] = str(action).replace(",", "\n")
            table.append(i)
        print_table_dict(fields, result.data, 'id')



