import requests
from pprint import pprint
from ..common import api
from ..common.utils import print_table_list
import json


def _get_bvc_flows(ctl, bapi, node, debug=False):
    #TODO fix key in output
    resource = api.API[bapi].format(server=ctl.server, table=0, node=node)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return(("Error connecting to BVC {}").format(ctl.server), False)
    return retval


def show_flows(session, args):
        debug = args['--debug']
        node = args['<node>']
        retval = _get_bvc_flows(session, 'FLOWS', node, debug)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            if debug:
                pprint(data)
            flowlist = []
            for i in data['flow-node-inventory:table']:
                if i is not None:
                    # for flow in i:
                    flowid = i.get('id')
                    flows = i.get('flow')
                    flowstats = i.get('opendaylight-flow-statistics:aggregate-flow-statistics')
                    tablestats = i.get('opendaylight-flow-table-statistics:flow-table-statistics')

                    for flow in flows:
                        fmatch = flow.get('match')
                        finstructions = flow.get('instructions').get('instruction')
                        flow = {'id': flow.get('id'),
                                         'cookie': flow.get('cookie'),
                                         'idle-timeout': flow.get('idle-timeout'),
                                         'hard-timeout': flow.get('hard-timeout'),
                                         'priority': flow.get('priority'),
                                         'table_id': flow.get('table_id'),
                                         'flags': flow.get('flags'),
                                         'match': json.dumps(fmatch),
                                         # 'instructions': finstructions,
                                         }
                        # fmatch = dict(zip(fmatch.keys(), fmatch.values()))
                        # z = dict(flow.items() + fmatch.items())
                        flowlist.append(flow)

                    if flowlist is not None:
                        print_table_list('Flows', flowlist, 'id')

        else:
            print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)
