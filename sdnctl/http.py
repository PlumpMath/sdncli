"""
Usage:
        sdncli http [options] get <resource>
        sdncli http [options] delete <resource>
        sdncli http [options] post <resource> (--payload <payload>> | --file <file>)
        sdncli http [options] put <resource> (-payload <payload>>  | --file <file>)

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
import json
import util
from pybvc.common import status
from pybvc.common.status import STATUS
from pybvc.common.result import Result
from pybvc.common.result import OperStatus


def http(ctl, args):
    # GET
    if args.get('get'):
        result = http_get(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                raise ValueError(response=(result.data))
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    #PUT
    elif args.get('put'):
        result = http_put(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                print "Succes.. No data.."
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    #POST
    elif args.get('post'):
        result = http_post(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                raise ValueError(response=(result.data))
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    #DELETE
    elif args.get('delete'):
        result = http_delete(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                    print "Succes.. No data.."
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)


def http_get(ctl, args):
    ignore = args['--force']
    import hashlib
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    status = OperStatus()
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
    elif(resp.status_code == 200 or resp.status_code == 204):
        status.set_status(STATUS.OK)
    else:
        status.set_status(STATUS.HTTP_ERROR, resp)
    return Result(status, resp)


def http_post(ctl, args):
    if args['--payload']:
        payload = args['<payload>']
    elif args['--file']:
        payload = util.load_json_file(args['<file>'])
    status = OperStatus()
    headers = {'content-type': 'application/yang.data+json',
               'accept': 'text/json, text/html, application/xml, */*'}
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = ctl.http_post_request(url, json.dumps(payload), headers)
    if(resp is None):
        status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
        status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200 or resp.status_code == 204):
        status.set_status(STATUS.OK)
    else:
        status.set_status(STATUS.HTTP_ERROR, resp)
    return Result(status, resp)


def http_put(ctl, args):
    if args['--payload']:
        payload = args['<payload>']
    elif args['--file']:
        payload = util.load_json_file(args['<file>'])
    status = OperStatus()
    headers = {'content-type': 'application/yang.data+json',
               'accept': 'text/json, text/html, application/xml, */*'}
    templateUrl = "http://{}:{}/restconf/{}"
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = ctl.http_put_request(url, json.dumps(payload), headers)
    if(resp is None):
        status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
        status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200 or resp.status_code == 204):
        status.set_status(STATUS.OK)
    else:
        status.set_status(STATUS.HTTP_ERROR, resp)
    return Result(status, resp)

    # if(resp is None):
    #         status.set_status(STATUS.CONN_ERROR)
    # elif(resp.content is None):
    #         status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    # elif(resp.status_code == 200):
    #     print "Success"


def http_delete(ctl, args):
    ignore = args['--force']
    templateUrl = "http://{}:{}/restconf/{}"
    status = OperStatus()
    url = templateUrl.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
    resp = ctl.http_delete_request(url, data=None, headers=None)
    if(resp is None):
        status.set_status(STATUS.CONN_ERROR)
    elif(resp.content is None):
        status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    elif(resp.status_code == 200 or resp.status_code == 204):
        status.set_status(STATUS.OK)
    else:
        status.set_status(STATUS.HTTP_ERROR, resp)
    return Result(status, resp)
    # if(resp is None):
    #         status.set_status(STATUS.CONN_ERROR)
    # elif(resp.content is None):
    #         status.set_status(STATUS.CTRL_INTERNAL_ERROR)
    # elif(resp.status_code == 200):
    #     print resp.json()

