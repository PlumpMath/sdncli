"""
Usage:
        sdncli http [options] get <resource>
        sdncli http [options] delete <resource>
        sdncli http [options] post <resource> ([--payload <payload>] | [--file <file>])
        sdncli http [options] put <resource> ([--payload <payload>] | [--file <file>])

Options :
            -d --debug             Print JSON dump
            -h --help              This help screen
            -f --force             Ignore cache
            -y --yang              Utilize yang mounted prefix
            -o --operational       Read from operational datastore
            -p --operations        RPC Resource
            -c --config            Read from configuration datastore
            -s --streams           Read from streams

            Resources:
            opendaylight-inventory:nodes/node/{node}/yang-ext:mount

"""
from requests import ConnectionError
from pprint import pprint
import json
import os
import pybvc.common.status


def http(ctl, args):
    # GET
    if args.get('get'):
        http_get(ctl, args)
    elif args.get('put'):
        http_put(ctl, args)
    elif args.get('delete'):
        http_delete(ctl, args)


def http_get(ctl, args):
    ignore = args['--force']
    import hashlib
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
  
    # resourcehash = int(hashlib.md5(resource).hexdigest(), 16)
    # if not (os.path.exists(utils.get_cachedir())):
    #     utils.prepare_directory(utils.get_cachedir())
    # filename = os.path.join(utils.get_cachedir(), str(resourcehash))
    # (buf, status) = utils.check_file_and_print(filename)
    # if ignore or not status:
    # retval = _http_get(ctl, resource)

    resp = ctl.http_get_request(url, data=None, headers=None)
    if(resp is None):
            status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200):
        print resp.json()

    #     if str(retval.status_code)[:1] == "2":
    #         # utils.write_file(str(resourcehash), utils.get_cachedir(), json.dumps(retval.response))
    #         pprint(retval.json())
    #     else:
    #         print("Houston we have a problem, {} {}").format(retval.status_code, retval.reason)
    # else:
    #     #TODO add async cache refresh
    #     print buf


def http_post(ctl, args):
    if args['--payload']:
        payload = args['<payload>']
    elif args['--file']:
        payload = utils.load_json_file(file)

    headers = {'content-type': 'application/yang.data+json',
               'accept': 'text/json, text/html, application/xml, */*'}
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = self.http_post_request(url, json.dumps(payload), headers)
    if(resp is None):
            status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200):
        print resp.json()


def http_put(ctl, args):
    if args['--payload']:
        payload = args['<payload>']
    elif args['--file']:
        payload = utils.load_json_file(args['<file>'])
    headers = {'content-type': 'application/yang.data+json',
               'accept': 'text/json, text/html, application/xml, */*'}
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = ctl.http_put_request(url, json.dumps(payload), headers)
    if(resp is None):
            status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200):
        print "Success"


def http_delete(ctl, args):
    ignore = args['--force']
    templateUrl = "http://{}:{}/restconf/{}"

    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = ctl.http_delete_request(url, data=None, headers=None)
    if(resp is None):
            status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
            status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200):
        print resp.json()

#TODO Create higher abstraction for YANG Mounts
