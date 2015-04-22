import requests
from uuid import uuid4
# from pprint import pprint
from ..common import api
from ..common import utils
from ..netconf import netconflib


def _mount_netconf_device(ctl, name, node, user, pw, port=830, mlx=None):
        if mlx:
            data = netconflib.netconf_mount_mlx(name, node, port, user, pw)
        else:
            data = netconflib.netconf_mount(name, node, port, user, pw)
        resource = api.API['MOUNTDEVICE'].format(server=ctl.server)
        headers = {'content-type': 'application/xml'}
        try:
            retval = ctl.session.post(resource, auth=ctl.auth, params=None, headers=headers, data=data)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(ctl.server), False)
        if str(retval.status_code)[:1] == "2":
            return(("Mounted Node {} on {}").format(name, node), True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)


def mount_device(ctl, args):
        if args['--port']:
            port = args['<port>']
        else:
            port = 830
        (retval, status) = _mount_netconf_device(ctl, args['<node>'], args['<address>'], args['<username>'], args['<password>'], port, args['--mlx'])
        if status:
            print(retval)
        else:
            print("Houston we have a problem, {}").format(retval)


def _unmount_netconf_device(ctl, name):
        resource = api.API['UNMOUNTDEVICE'].format(server=ctl.server, name=name)
        headers = {'content-type': 'application/xml'}
        try:
            retval = ctl.session.delete(resource, auth=ctl.auth, params=None, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Error connecting to BVC {}").format(ctl.server)
            return None
        if str(retval.status_code)[:1] == "2":
            return(("UnMounted Node {}").format(name), True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)


def unmount_device(ctl, args):
    (retval, status) = _unmount_netconf_device(ctl, args['<node>'])
    if status:
        print(retval)
    else:
        print("Houston we have a problem, {}").format(retval)


def _get_mount_status(ctl, debug=False):
        stats = {}
        # keys = {"netconf-node-inventory"}
        resource = api.API['OPER'].format(server=ctl.server)
        headers = {'content-type': 'application/xml'}
        try:
            retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=headers)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(ctl.server), False)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            root = data['nodes']['node']
            for line in root:
                if 'netconf-node-inventory:connected' not in line:
                    stats.update({line['id']: False})
                elif 'netconf-node-inventory:connected' in line:
                    stats.update({line['id']: line['netconf-node-inventory:connected']})
            return (stats, True)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)


def _get_mounts(ctl, debug=False):
        mountdb = {}
        (retval, status) = _get_mount_status(ctl, debug)
        mntstats = retval
        if status:
            keys = {"odl-sal-netconf-connector-cfg:sal-netconf-connector"}
            resource = api.API['MOUNTS'].format(server=ctl.server)
            headers = {'content-type': 'application/xml'}
            try:
                retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=headers)
            except requests.exceptions.ConnectionError:
                return(("Error connecting to BVC {}").format(ctl.server), False)
            if str(retval.status_code)[:1] == "2":
                data = retval.json()
                # if debug:
                #     pprint(data)
                root = data['config:modules']['module']
                for line in root:
                    if line['type'] in keys:
                        mountmap = {'name':     line['name'],
                                    'address':  line['odl-sal-netconf-connector-cfg:address'],
                                    'port':     line['odl-sal-netconf-connector-cfg:port'],
                                    'username': line['odl-sal-netconf-connector-cfg:username'],
                                    'password': line['odl-sal-netconf-connector-cfg:password'],
                                    'connected':   mntstats[line['name']]
                                    }
                        mountdb.setdefault(str(uuid4()), []).append(mountmap)
                if len(mountdb) > 0:
                    return(mountdb, True)
                else:
                    return("No Mounts found", False)
            else:
                return (("Unexpected Status Code {}").format(retval.status_code), False)
        else:
                return (("{}").format(retval), False)


def show_mounts(ctl, debug=False):
        (retval, status) = _get_mounts(ctl, debug)
        if status:
            utils.print_table("mounts", retval, 'name')
        else:
            print("Houston we have a problem, {}").format(retval)
