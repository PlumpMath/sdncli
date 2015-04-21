from api import API
import requests
# from uuid import uuid4
from pprint import pprint
# from utils import print_table


def _netconf_get(ctl, node, ds, api):
    resource = API[api].format(server=ctl.server, node=node, ds=ds)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers,  timeout=120)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to BVC {}").format(ctl.server), False)
    if str(retval.status_code)[:1] == "2":
        try:
            data = retval.json()
        except ValueError, e:
            return(("Bad JSON found: {} {}").format(e, retval.text), False)
        return(data, True)
    else:
        return (("Unexpected Status Code {}").format(retval.status_code), False)


def get_config(ctl, node, ops, debug=False):
    if(ops):
        ds = 'operational'
    else:
        ds = 'config'
    (retval, status) = _netconf_get(ctl, node, ds, 'NETCONF')
    if status:
        pprint(retval)
    else:
        print("Houston we have a problem, {}").format(retval)
