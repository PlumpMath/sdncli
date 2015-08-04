"""
Usage:
        bvcctl node mount <node> <address> <username> <password> [--port <port>] [--mlx]
        bvcctl node unmount <node>

Options :
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""
from pybvc.controller.netconfnode import NetconfNode
from pybvc.common.status import STATUS


def node(ctl, args):
    if args.get('mount'):
        addr = args.get('<address>')
        name = args.get('<node>')
        port = args.get('<port>')
        user = args.get('<username>')
        pw = args.get('<password>')
        nodeid = ctl.inventory.get_netconf_node(name)
        if not nodeid:
            node = NetconfNode(ctl, name, addr, user, pw, portNum=port)
            print node.to_json()
            result = ctl.add_netconf_node(node)
            status = result.get_status()
            if(status.eq(STATUS.OK)):
                result = ctl.check_node_conn_status(node)
                if(status.eq(STATUS.OK)):
                    print "Mounted node {}".format(name)
            else:
                print "Houston we have a problem: {}".format(status.to_string())
        else:
                print "Node: {} is already in inventory".format(name)
    elif args.get('unmount'):
        name = args.get('<node>')
        nodeid = ctl.inventory.get_netconf_node(name)
        if nodeid:
            result = ctl.delete_netconf_node(nodeid)
            if(result.status.eq(STATUS.OK)):
                print "UnMounted Node {}".format(name)
        else:
                print "Node: {} is not in inventory".format(name)
