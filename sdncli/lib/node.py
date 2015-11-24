"""
Usage:
        sdncli node mount <node> <address> <username> <password> [(--ssh <enable> <type>)] [--port <port>]
        sdncli node command <node> <template> <command>
        sdncli node unmount <node> [--ssh]
        sdncli node command <node> <command>

Options :
            -h --help                   This help screen.
            -o --operations             Read from operations datastore.
            -p <port>  --port <port>    Mount port [default: 1830].

"""
import json
from pprint import pprint
from pybvc.controller.netconfnode import NetconfNode
from pybvc.common.status import STATUS

headers = {'content-type': 'application/json',
           'accept': 'application/json'}


def node(ctl, args):
    # MOUNT
    if args.get('mount'):
        if args.get('--ssh'):
            mount_ssh(ctl, args)
            return
        addr = args.get('<address>')
        name = args.get('<node>')
        port = args.get('<port>')
        user = args.get('<username>')
        pw = args.get('<password>')
        if port is None:
            port = 830
        nodeid = ctl.inventory.get_netconf_node(name)
        if nodeid is None:
            node = NetconfNode(ctl, nodeName=name, ipAddr=addr, portNum=port,
                               adminName=user, adminPassword=pw)
            result = ctl.add_netconf_node(node)
            if(result.status.eq(STATUS.OK)):
                print "Mounted node {}".format(name)
            else:
                print "Houston we have a problem {}".format(result.get_status().to_string())
        else:
            print "Node: {} is already in inventory".format(name)
    # UNMOUNT
    elif args.get('unmount'):
        if args.get('--ssh'):
            unmount_ssh(ctl, args)
            return
        name = args.get('<node>')
        # TODO figure out where nodes live.
        # result = [ctl.delete_netconf_node(nodeid) for nodeid in ctl.inventory.netconf_nodes if nodeid.get_id() == name]
        result = ctl.delete_netconf_node(name)
        if(result.status.eq(STATUS.OK)):
                print "UnMounted Node {}".format(name)
        else:
                print "Houston we have a problem {}".format(result.get_status().to_string())
    # COMMAND
    elif args.get('command'):
        name = args.get('<node>')
        template = args.get('<template>')
        command = args.get('<command>')
        result = execute_command(ctl, name, template, command)
        pprint(result)
        # if(result.status.eq(STATUS.OK)):
        #     print "UnMounted Node {}".format(name)
        # else:
        #     print "Node: {} is not in inventory".format(name)


def add_platform(ctl, name, addr, user, pw, enable, devtype):
    addplatform = {'input': {'name': name, 'ip-address': addr,
                             'username': user, 'password': pw,
                             'enable-password': enable, 'type': devtype}}
    pprint(json.dumps(addplatform))
    template_url = "http://{}:{}/restconf/operations/cliconf:add-platform".format(ctl.ipAddr, ctl.portNum)
    print template_url
    # response = ctl.http_post_request(template_url, json.dumps(addplatform), headers=None)
    response = ctl.http_post_request(template_url, json.dumps(addplatform), headers=headers)
    print "Add Platform"
    pprint(response.content)
    return True if response.status_code == 200 else False


def mount_ssh(ctl, args):
    addr = args.get('<address>')
    name = args.get('<node>')
    user = args.get('<username>')
    pw = args.get('<password>')
    enable = args.get('<enable>')
    devtype = args.get('<type>')
    nodeid = ctl.inventory.get_netconf_node(name)
    if nodeid is None:
        if(add_platform(ctl, name, addr, user, pw, enable, devtype)):
            print "Mounted Device {}".format(name)
            # sshmount = {'input': {'device-name': name}}
            # template_url = "http://{}:{}/restconf/operations/cliconf:mount-device".format(ctl.ipAddr, ctl.portNum)
            # response = ctl.http_post_request(template_url, json.dumps(sshmount), headers=headers)
            # # pprint(response.content)
            # if(response.status_code == 200):
            #     print "Mounted node {}".format(name)
            #     # execute_command(name, 'connection-template')
        else:
            print "Error adding platform {}".format(devtype)
    else:
        print "Node: {} is already in inventory".format(name)


def unmount_ssh(ctl, args):
    name = args.get('<node>')
    # nodeid = ctl.inventory.get_netconf_node(name)
    # if nodeid is None:
    ssh_unmount = {'input': {'name': name, }}
    template_url = "http://{}:{}/restconf/operations/cliconf:remove-platform".format(ctl.ipAddr, ctl.portNum)
    response = ctl.http_post_request(template_url, json.dumps(ssh_unmount), headers)
    pprint(response)
    # TODO not getting an error code on unmount bad name
    if(response.status_code == 200):
        print "UnMounted node {}".format(name)
    # else:
    #         print "Node: {} not found in inventory".format(name)


def execute_command(ctl, node, template_name, command):
        ssh_command = {'input': {'device-name': node,
                                 'template-connection-name': template_name,
                                 'extensive-output': 'true',
                                 'command': [{'do-command': command,
                                              }]}}
        print ssh_command
        template_url = "http://{}:{}/restconf/operations/cliconf:execute-commands".format(ctl.ipAddr, ctl.portNum)
        response = ctl.http_post_request(template_url, json.dumps(ssh_command), headers=headers)
        pprint(response)
        if(response.status_code == 200):
            print "executed command {}".format(command)
        else:
            print "Failed to execute command on {} ".format(node)
