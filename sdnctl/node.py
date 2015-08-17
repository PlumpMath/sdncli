"""
Usage:
        sdncli node mount <node> <address> <username> <password> [--port <port>] [--ssh <enable> <type>]
        sdncli node unmount <node>

Options :
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""
from pybvc.controller.netconfnode import NetconfNode
from pybvc.common.status import STATUS
from time import sleep
from pybvc.netconfdev.vrouter.vrouter5600 import VRouter5600


def node(ctl, args):
    #MOUNT
    if args.get('mount'):
        if args.get('--ssh'):
            mount_ssh(ctl, args)
            return
        addr = args.get('<address>')
        name = args.get('<node>')
        port = args.get('<port>')
        user = args.get('<username>')
        pw = args.get('<password>')
        nodeid = ctl.inventory.get_netconf_node(name)
        if nodeid is None:
            node = NetconfNode(ctl, name, addr, user, pw, portNum=port)
            result = ctl.add_netconf_node(node)
            if(result.status.eq(STATUS.OK)):
                print "Mounted node {}".format(name)
        else:
                print "Node: {} is already in inventory".format(name)
    #UNMOUNT
    elif args.get('unmount'):
        name = args.get('<node>')
        nodeid = ctl.inventory.get_netconf_node(name)
        if nodeid:
            result = ctl.delete_netconf_node(nodeid)
            if(result.status.eq(STATUS.OK)):
                print "UnMounted Node {}".format(name)
        else:
                print "Node: {} is not in inventory".format(name)


def mount_ssh(ctl, args):
        addr = args.get('<address>')
        name = args.get('<node>')
        port = args.get('<port>')
        user = args.get('<username>')
        pw = args.get('<password>')
        enable = args.get('<enable>')
        devtype = args.get('<type>')
        resource = "operations/cliconf:add-platform"
        nodeid = ctl.inventory.get_netconf_node(name)
        in_put = """
                input : {
                    name: {name},
                    ip-address: {addr},
                    username: {user},
                    password: {pw},
                    enable-password: {enable},
                    type: {devtype}
                  }
        """
        print in_put.format(name=name, user=user, pw=pw, enable=enable, devtype=devtype)

