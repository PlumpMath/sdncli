from ..common import api
from ..httplib import httplib
from ..common.utils import print_table_list
from pprint import pprint


def show_api(ctl):
    apitable = []
    for k, v in api.API.viewitems():
        s = {'API': k, 'Link': v}
        apitable.append(s)
    print_table_list("API", apitable)


def show_ctl_apis(ctl):
    apitable = []
    resource = api.API['CTLAPIS'].format(server=ctl.server)
    retval = httplib._http_get(ctl, resource, payload=None)
    if retval.status_code == 200:
        data = retval.json()
        root = data['apis']
        for i in root:
            s = {'CTLAPI': i['path']}
            apitable.append(s)
        print_table_list('CTLAPI', apitable)
    else:
        print("Houston we have a problem, {}").format(retval)
