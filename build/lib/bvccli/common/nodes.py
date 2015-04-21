from api import API
import requests
from uuid import uuid4
from pprint import pprint
from utils import print_table


def _get_bvc_nodes(ctl, ds, debug=False):
    #TODO fix key in output
    nodetable = {}
    filter_keys = ('controller-config')
    resource = API[ds].format(server=ctl.server)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return(("Error connecting to BVC {}").format(ctl.server), False)
    if str(retval.status_code)[:1] == "2":
        data = retval.json()
        if debug:
            pprint(data)
        [nodetable.update({line['id']: ds.lower()}) for line in data['nodes']['node'] if line['id'] not in filter_keys]
    if len(nodetable) > 0:
        return (nodetable, True)
    else:
        return (("No Nodes Found").format(retval.status_code), False)


def show_nodes(session, debug=False):
        nodemap = {}
        nodetable = {}
        (retval, status) = _get_bvc_nodes(session, 'OPER', debug)
        if status:
            node_ops = retval
            (retval, status) = _get_bvc_nodes(session, 'CONFIG', debug)
            if status:
                node_config = retval
                nodemap = node_ops.copy()
                nodemap.update(node_config)
            else:
                nodemap = node_ops

            for n in nodemap:
                s = {'node': n, 'status': nodemap[n]}
                nodetable.setdefault(uuid4(), []).append(s)
            print_table("get_nodes:", nodetable)
        else:
            print("Error: {}").format(retval)
