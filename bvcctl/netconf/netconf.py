import requests
from pprint import pprint
from uuid import uuid4
from ..common import api
from ..common import utils
import os
import json
import hashlib


def _netconf_get(ctl, node, ds, apicall, debug, resource=None):
    if resource is not None:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource=resource)
    else:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource="")
    try:
        retval = ctl.session.get(call, auth=ctl.auth, params=None, headers=ctl.headers,  timeout=120)
        if debug:
            pprint(retval.text)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to BVC {}").format(ctl.server), False)
    return retval


def _netconf_delete(ctl, node, ds, apicall, debug, resource=None):
    if resource is not None:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource=resource)
    else:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource="")
    try:
        retval = ctl.session.delete(call, auth=ctl.auth, params=None, headers=ctl.headers, timeout=120)
        if debug:
            pprint(retval.text)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to BVC {}").format(ctl.server), False)
    return retval


def _netconf_post(ctl, node, ds, apicall, debug, payload=None, resource=None):
    if resource is not None:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource=resource)
    else:
        call = api.API[apicall].format(server=ctl.server, node=node, ds=ds, resource="")
    try:
        retval = ctl.session.post(call, auth=ctl.auth, params=None, headers=ctl.headers, data=payload, timeout=120)
        if debug:
            pprint(retval.text)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to BVC {}").format(ctl.server), False)
    return retval


def get_capabilities(ctl, node):
    resource = api.API['CAPABILITIES'].format(server=ctl.server, node=node)
    headers = {'content-type': 'application/xml'}
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=headers)
    except requests.exceptions.ConnectionError:
        raise requests.ConnectionError("Error connecting to server")
    return retval


def get_schemas(ctl, args):
    #TODO: Test for ietf-monitoring first
    debug = args['--debug']
    verbose = args['--verbose']
    pyang = args['--pyang']
    #TODO What is the difference between operational and operations?
    ds = 'operations'
    node = args['<node>']
    retval = get_capabilities(ctl, node)
    if retval.status_code == 200:
        data = retval.json()
        for i in data['netconf-state']['schemas']['schema']:
            module = i['namespace'].rsplit(':', 1)[1]
            revision = i['version'] or None
            data = {'input': {'identifier': module}}
            retval = _netconf_post(ctl, node, ds, 'GETSCHEMA', debug, payload=json.dumps(data))
            if retval.status_code == 200:
                data = retval.json()['get-schema']['output']['data']
                if verbose:
                    print os.path.join(utils.get_schemadir(), module)
                if pyang:
                    utils.print_file((module + '.yang'), utils.get_schemadir(), json.dumps(data))
                if revision:
                    utils.print_file((module + '@' + revision), utils.get_schemadir(), json.dumps(data))
                else:
                    utils.print_file((module), utils.get_schemadir(), json.dumps(data))
            else:
                print("Houston we have a problem, {}").format(retval)
    else:
        print("Houston we have a problem, {}").format(retval)


def show_capabilities(ctl, args):
    debug = args['--debug']
    node = args["<node>"]
    moduledb = {}
    retval = get_capabilities(ctl, node)
    if str(retval.status_code)[:1] == "2":
        data = retval.json()
        if debug:
            pprint(data)
        try:
            root = data['netconf-state']['schemas']['schema']
            for line in root:
                modulemap = {'namespace': line['namespace'],
                             'revision':  line['version']}
                moduledb.setdefault(str(uuid4()), []).append(modulemap)
            if len(moduledb) > 0:
                utils.print_table("Node Capabilities", moduledb, 'namespace')
            else:
                return(("No Modules found for Node: {}").format(node), False)
        except KeyError:
            return(("Error in schema for Node: {}").format(node), False)
    else:
        return (("Unexpected Status Code {}").format(retval.status_code), False)


def show_config(ctl, args):
    debug = args['--debug']
    node = args['<node>']
    ignore = args['--force']
    if(args['--config']):
        ds = 'config'
    else:
        ds = 'operational'
    urihash = int(hashlib.md5(os.path.join(utils.get_configdir(), node)).hexdigest(), 16)
    filename = os.path.join(utils.get_configdir(), str(urihash))
    (buf, status) = utils.check_file_and_print(filename)
    if status:
        print "Loading from cache file: {}".format(filename)
    if ignore or not status:
        retval = _netconf_get(ctl, node, ds, 'NETCONF', debug)
        if retval.status_code == 200:
            pprint(retval.text)
            utils.write_file(str(urihash), utils.get_configdir(), json.dumps(retval.json()))
            pprint(retval.json())
        else:
            print("Houston we have a problem, {}").format(retval)
    else:
        jdata = json.loads(buf)
        print(jdata)


def show_schema(ctl, args):
    debug = args['--debug']
    ds = 'operations'
    module = args['<resource>']
    data = {'input': {'identifier': module}}
    retval = _netconf_post(ctl, args['<node>'], ds, 'GETSCHEMA', debug, data)
    if str(retval.status_code)[:1] == "2":
        print retval.json()['get-schema']['output']['data']
    else:
        print("Houston we have a problem, {}").format(retval)
