"""
Usage:
        bvcctl show flows <node> 
        bvcctl show flow <id> 
        bvcctl show hosts
        bvcctl show mounts
        bvcctl show nodes
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
# from pybvc.controller.topology import Topology


def show(ctl, args):
    if args.get('nodes'):
        # s = [i.to_json() for i in ctl.inventory.netconf_nodes]
        status = ctl.get_all_nodes_conn_status()
        print status.data 
    elif args.get('hosts'):
        print ctl.topology.to_string()
        # for node in ctl.topology.get_hosts():
        #     print node.get_id()
        #     print node.get_mac_address()
        #     print node.get_openflow_id()
        #     # addr = node.get('host_tracker_service:addresses')
        #     # if ("host_tracker_service:addresses" in node):

    elif args.get('mounts'):
        pass
        # TODO add predicate
        # print [vars(i) for i in ctl.inventory.data.netconf_nodes]
    elif args.get('topology'):
        print "show topology"
    elif args.get('modules'):
        print ctl.get_config_modules().data
    elif args.get('streams'):
        print ctl.get_streams_info().data
    elif args.get('providers'):
        print ctl.get_service_providers_info().data
    elif args.get('openflow'):
        nodes = ctl.build_inventory_object().data
        for i in nodes.openflow_nodes:
            print vars(i)

