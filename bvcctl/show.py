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
from util import print_table_list
from util import print_table_dict
from pprint import pprint
from pybvc.common.status import STATUS
import json

# from pybvc.controller.topology import Topology


def show(ctl, args):
    if args.get('nodes'):
        s = ctl.topology
        pprint(vars(s))
        print_table_list('Nodes', ctl.topology.nodes)
    elif args.get('hosts'):
        print ctl.topology.hosts
        print_table_list('Hosts', ctl.topology.hosts)
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
        modules = []
        result = ctl.get_config_modules()
        if(result.status.eq(STATUS.OK)):
            modulelist = result.data
            pprint(modulelist)
            for line in modulelist:
                    modulemap = {'type':     line['type'],
                                 'name': line['name']}
                    modules.append(dict(modulemap))
            print_table_dict('Modules', modules)



    elif args.get('streams'):
        print ctl.get_streams_info().data
    elif args.get('providers'):
        print ctl.get_service_providers_info().data
    elif args.get('openflow'):
        nodes = ctl.build_inventory_object().data
        for i in nodes.openflow_nodes:
            print vars(i)

