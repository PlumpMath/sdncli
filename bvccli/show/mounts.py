import requests
from uuid import uuid4
# from pprint import pprint
from ..common import api
from ..common import utils
from pprint import pprint


def _get_mount_status(ctl, debug=False):
        stats = []
        vals = []
        # keys = {"netconf-node-inventory"}
        resource = api.API['OPER'].format(server=ctl.server)
        try:
            retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(ctl.server), False)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            root = data['nodes']['node']
            keys = ['id', 'connected', 'type']
            for line in root:
                devid = line['id']
                if 'netconf-node-inventory:connected' in line:
                    connected = True
                else:
                    connected = False
                for l in line['netconf-node-inventory:initial-capability']:
                    if devid == "controller-config":
                        devtype = 'controller'
                    elif "brocade-interface" in l:
                        devtype = 'nos'
                        break
                    elif "vyatta-interfaces" in l:
                        devtype = 'vyatta'
                        break
                    elif "vyatta-interfaces" in l:
                        devtype = 'vyatta'
                        break
                    else:
                        devtype = 'unknown'
                vals = [devid, connected, devtype]
                stats.append(dict(zip(keys, vals)))
            return stats
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)


def get_mounts(ctl, debug=False):
        resource = api.API['MOUNTS'].format(server=ctl.server)
        try:
            retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers)
        except requests.exceptions.ConnectionError:
            raise requests.ConnectionError("Error connecting to BVC {}").format(ctl.server)
        return retval
        #     if str(retval.status_code)[:1] == "2":


def get_mounts_connected(devid, stats):
    for line in stats:
        if line.get('id') == devid:
            return line.get('connected')


def get_mounts_type(devid, stats):
    for line in stats:
        if line.get('id') == devid:
            return line.get('type')


def show_mounts(ctl):
        mountdb = []
        keys = ['name', 'address', 'port', 'username', 'password', 'connected', 'type']
        select = {"odl-sal-netconf-connector-cfg:sal-netconf-connector"}
        mntstats = _get_mount_status(ctl)
        retval = get_mounts(ctl)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            # if debug:
            #     pprint(data)
            root = data['config:modules']['module']
            for line in root:
                if line['type'] in select:
                    vals = [line['name'],
                            line['odl-sal-netconf-connector-cfg:address'],
                            line['odl-sal-netconf-connector-cfg:port'],
                            line['odl-sal-netconf-connector-cfg:username'],
                            line['odl-sal-netconf-connector-cfg:password'],
                            get_mounts_connected(line['name'], mntstats),
                            get_mounts_type(line['name'], mntstats)
                            ]
                    mountdb.append(dict(zip(keys, vals)))
            if len(mountdb) > 0:
                return mountdb
            else:
                return("No Mounts found", False)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)
