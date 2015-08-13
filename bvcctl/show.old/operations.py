import requests
from uuid import uuid4
from pprint import pprint
from ..common import utils
from ..common import api


def _get_operations(ctl, node, debug=False):
        moduledb = {}
        resource = api.API['OPERATIONS'].format(server=ctl.server, node=node)
        try:
            retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers)
        except requests.exceptions.ConnectionError:
            return(("Error connecting to BVC {}").format(ctl.server), False)
        if str(retval.status_code)[:1] == "2":
            data = retval.json()
            if debug:
                pprint(data)
            return (data, True)
            # root = data['modules']['module']
            # for line in root:
            #     modulemap = {'name':     line['name'],
            #                  'namespace': line['namespace'],
            #                  'revision':  line['revision']}
            #     moduledb.setdefault(str(uuid4()), []).append(modulemap)
            # if len(moduledb) > 0:
            #     return(moduledb, True)
            # else:
            #     return("No Modules found", False)
        else:
            return (("Unexpected Status Code {}").format(retval.status_code), False)


def show_operations(ctl, args):
        debug = args['--debug']
        node = args['<node>']
        (retval, status) = _get_operations(ctl, node, debug)
        if status:
            utils.print_table_keys("show-operations", "operations", retval)
        else:
            print("Houston we have a problem, {}").format(retval)
