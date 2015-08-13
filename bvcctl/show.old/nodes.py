import requests
from uuid import uuid4
from pprint import pprint
from ..common import utils
from ..common import api


def _get_bvc_nodes(ctl, ds, debug=False):
    #TODO fix key in output
    nodetable = {}
    filter_keys = ('controller-config')
    resource = api.API[ds].format(server=ctl.server)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, 
                 headers=ctl.headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return(("Error connecting to BVC {}").format(ctl.server), False)
    return retval
    # if str(retval.status_code)[:1] == "2":
    #     data = retval.json()
    #     if debug:
    #         pprint(data)
    #     [nodetable.update({line['id']: ds.lower()}) for line in data['nodes']['node'] if line['id'] not in filter_keys]
    # if len(nodetable) > 0:
    #     return (nodetable, True)
    # else:
    #     return (("No Nodes Found").format(retval.status_code), False)


def show_nodes(session, args):
        debug = args['--debug']
        nodemap = {}
        nodekeys={'node', 'operational', 'config'}
        nodetable = []
        filter_keys = ('controller-config')

        retval = _get_bvc_nodes(session, 'OPER', debug)
        oper = retval.json()
        if retval.status_code == 200:
            retval = _get_bvc_nodes(session, 'CONFIG', debug)
            config = retval.json()
            if retval.status_code == 200:
                print config['nodes']['node']
            # data = retval.json()
            # [nodetable.append({'node': line['id'], 'oper': True}) for line in oper['nodes']['node'] for y in config['nodes']['node'] if line['id'] not in filter_keys]
                s = [x for x in oper['nodes']['node'] for y['id'] in config['nodes']['node'] if y['id'] not in filter_keys]
                print s
            #     data = retval.json()
            #     [nodetable.['config'] : True} for line in data['nodes']['node'] if line['id'] = node]
            #     # [nodetable.append({'node' : line['id'], 'oper' : None, 'config': True}) for line in data['nodes']['node'] if line['id'] = node]
            #     print nodetable
            #     # nodemap = node_ops.copy()
            #     # nodemap.update(node_config)
            # else: 
            #     # nodemap = node_ops
            #     print "error"

            # # for n in nodemap:
            # #     s = {'node': n, 'status': nodemap[n]}
            # #     nodetable.setdefault(uuid4(), []).append(s)
            # utils.print_table_list("get_nodes:", dict(zip(nodekeys,nodetable)))
        else:
             print("Error: {}").format(retval)
