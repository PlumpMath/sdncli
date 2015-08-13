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
            # Need to wait for mount
            # sleep(5)
            # if(result.status.eq(STATUS.OK)):
            #     result = ctl.check_node_conn_status(node)
            #     # TODO Fix this
            #     if(result.status.eq(STATUS.OK)):

            #         # Device Detection.. Move into pysdn..
            #         # result = node.get_schemas()
            #         # if(result.status.eq(STATUS.OK)):
            #         #     schemas = result.data
            #         #     for schema in schemas:
            #         #         if "controller-config" in schema['identifier']:
            #         #             devtype = 'controller'
            #         #             break
            #         #         elif "brocade-interface" in schema['identifier']:
            #         #             devtype = 'nos'
            #         #             break
            #         #         elif "vyatta-interfaces" in schema['identifier']:
            #         #             devtype = 'vyatta'
            #         #             vr = VRouter5600(ctl, name, addr, user, pw, port)
            #         #             break
            #         #         else:
            #         #             devtype = 'unknown'
            #         #             break
            #     else:
            #         print "Houston we have a problem: {}".format(status.to_string())
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

        # payload = json.loads(in_put)
        # print payload
        # if not nodeid:
        #     headers = {'content-type': 'application/yang.data+json',
        #                'accept': 'text/json, text/html, application/xml, */*'}
        #     templateUrl = "http://{}:{}/restconf/{}"
        #     url = templateUrl.format(ctl.ipAddr, ctl.portNum, resource)
        #     resp = ctl.http_post_request(url, json.dumps(payload), headers)
        #     if(resp is None):
        #             status.set_status(STATUS.CONN_ERROR)
        #     elif(resp.content is None):
        #             status.set_status(STATUS.CTRL_INTERNAL_ERROR)
        #     elif(resp.status_code == 200):
        #         print resp.json()
        # if 'netconf-node-inventory:initial-capability' in line:
        #     for l in line['netconf-node-inventory:initial-capability']:
        #         if devid == "controller-config":
        #             devtype = 'controller'
        #         elif "brocade-interface" in l:
        #             devtype = 'nos'
        #             break
        #         elif "vyatta-interfaces" in l:
        #             devtype = 'vyatta'
        #             break
        #         elif "vyatta-interfaces" in l:
        #             devtype = 'vyatta'
        #             break
        #         else:
        #             devtype = 'unknown'
        #     vals = [devid, connected, devtype]
        #     stats.append(dict(zip(keys, vals)))
