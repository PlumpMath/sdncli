from requests import ConnectionError
from ..common import utils
from ..common import api
from pprint import pprint
import json
import os


def _http_get(ctl, resource, payload=None):
        try:
            retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers, data=payload, timeout=120)
        except ConnectionError:
            raise ConnectionError("Error connecting to BVC")
        return retval


def _http_post(ctl, resource, file=None, payload=None):
        if file is not None:
            payload = utils.load_json_file(file)
        elif payload is not None:
            payload = json.loads(payload)
        try:
            retval = ctl.session.post(resource, auth=ctl.auth, params=None, headers=ctl.headers, data=json.dumps(payload), timeout=120)
        except ConnectionError:
            raise ConnectionError("Error connecting to BVC")
        return retval


def _http_put(ctl, resource, file=None, payload=None):
        if file is not None:
            payload = utils.load_json_file(file)
        elif payload is not None:
            payload = json.loads(payload)
        try:
            retval = ctl.session.put(resource, auth=ctl.auth, params=None, headers=ctl.headers, data=json.dumps(payload), timeout=120)
        except ConnectionError:
            raise ConnectionError("Error connecting to BVC")
        return retval


def _http_delete(ctl, resource):
        try:
            retval = ctl.session.delete(resource, auth=ctl.auth, params=None, headers=ctl.headers, timeout=120)
        except ConnectionError:
            raise ConnectionError("Error connecting to BVC")
        return retval


def http_get(ctl, args):
    import hashlib
    ignore = args['--force']
    if(args['--operational']):
        ds = "operational"
    elif(args['--streams']):
        ds = "streams"
    elif(args['--config']):
        ds = "config"
    else:
        ds = None
    if ds is not None:
        resource = api.API['BASE'].format(server=ctl.server, ds=ds, resource=ds + "/" + args['<resource>'])
    else:
        resource = api.API['BASE'].format(server=ctl.server, ds=ds, resource=args['<resource>'])
    resourcehash = int(hashlib.md5(resource).hexdigest(), 16)
    if not (os.path.exists(utils.get_cachedir())):
        utils.prepare_directory(utils.get_cachedir())
    filename = os.path.join(utils.get_cachedir(), str(resourcehash))
    (buf, status) = utils.check_file_and_print(filename)
    if ignore or not status:
        retval = _http_get(ctl, resource)
        if str(retval.status_code)[:1] == "2":
            # utils.write_file(str(resourcehash), utils.get_cachedir(), json.dumps(retval.response))
            pprint(retval.json())
        else:
            print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)
    else:
        #TODO add async cache refresh
        print buf


def http_post(ctl, args):
    if(args['--operational']):
        ds = "operational"
    if(args['--operations']):
        ds = "operations"
    else:
        ds = "config"
    resource = api.API['BASE'].format(server=ctl.server, ds=ds, resource=args['<resource>'])
    retval = _http_post(ctl, resource, args['<file>'], args['<payload>'])
    if str(retval.status_code)[:1] == "2":
        print("Success: {} {}").format(retval.status_code, retval.reason)
    else:
        print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)


def http_put(ctl, args):
    if(args['--operational']):
        ds = "operational"
    else:
        ds = "config"
    resource = api.API['BASE'].format(server=ctl.server, ds=ds, resource=args['<resource>'])
    retval = _http_put(ctl, resource, args['<file>'], args['<payload>'])
    if str(retval.status_code)[:1] == "2":
        print("Success: {} {}").format(retval.status_code, retval.reason)
    else:
        print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)


def http_delete(ctl, args):
    if(args['--operational']):
        ds = "operational"
    else:
        ds = "config"
    resource = api.API['BASE'].format(server=ctl.server, ds=ds, resource=args['<resource>'])
    retval = _http_delete(ctl, resource)
    if str(retval.status_code)[:1] == "2":
        print("Request Completed")
    else:
        print("Houston we have a problem, {}").format(retval.status_code)

#TODO Create higher abstraction for YANG Mounts
