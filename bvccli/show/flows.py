import requests
from pprint import pprint
from ..common import api


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
            pprint(retval.json())
        else:
            print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)
