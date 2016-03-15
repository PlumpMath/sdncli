"""
Usage:
        sdncli http [options] get <resource>
        sdncli http [options] delete <resource>
        sdncli http [options] post <resource> (--payload <payload> | --file <file>)
        sdncli http [options] put <resource> (-payload <payload>  | --file <file>)

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
from pysdn.common.status import STATUS
from pysdn.common.result import Result
from pysdn.common.result import OperStatus
from pysdn.common.utils import dict_unicode_to_string


def http(ctl, args):
    # GET
    if args.get('get'):
        result = http_get(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print(dict_unicode_to_string((result.get_data()).content))
            except ValueError:
                try:
                    # TODO Why is this JSON malformed?
                    print (result.get_data()).content.replace('\\\n', '')
                except ValueError:
                    print "Cannot coerece to JSON"
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    # PUT
    elif args.get('put'):
        result = http_put(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                print "Success.. No data.."
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    # POST
    elif args.get('post'):
        result = http_post(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                print "Success.. No data.."
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)
    # DELETE
    elif args.get('delete'):
        result = http_delete(ctl, args)
        if(result.status.eq(STATUS.OK)):
            try:
                print (result.data).json()
            except ValueError:
                    print "Success.. No data.."
        else:
            print "Error {}:{}".format(result.status.detailed(), result.data)


def http_get(ctl, args):
    # ignore = args['--force']
    # import hashlib
    template_url = "http://{}:{}/restconf/{}"
    url = template_url.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
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
    template_url = "http://{}:{}/restconf/{}"
    url = template_url.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
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
    template_url = "http://{}:{}/restconf/{}"
    url = template_url.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
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
    # ignore = args['--force']
    template_url = "http://{}:{}/restconf/{}"
    status = OperStatus()
    url = template_url.format(ctl.ipAddr, ctl.portNum, args['<resource>'])
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
