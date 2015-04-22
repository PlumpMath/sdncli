from requests import ConnectionError
from ..common import utils
import json
import os

# from ..common import utils


def _http_get(ctl, uri):
        headers = {'content-type': 'application/xml'}
        try:
            retval = ctl.session.get(uri, auth=ctl.auth, params=None, headers=headers, timeout=120)
        except ConnectionError:
            return(("Error connecting to BVC {}").format(ctl.server), False)
        if str(retval.status_code)[:1] == "2":
            try:
                data = retval.json()
            except ValueError, e:
                return(("Bad JSON found: {} {}").format(e, retval.text), False)
            return(data, True)
        else:
            return (("Unknown Status Code {}").format(retval.status_code), False)


def http_get(ctl, args):
    import hashlib
    ignore = args['--force']
    uri = args['<uri>']
    urihash = int(hashlib.md5(uri).hexdigest(), 16)
    if not (os.path.exists(utils.get_cachedir())):
        utils.prepare_directory(utils.get_cachedir())
    filename = os.path.join(utils.get_cachedir(), str(urihash))
    (buf, status) = utils.check_file_and_print(filename)
    if ignore or not status:
        (retval, status) = _http_get(ctl, uri)
        if status:
            utils.write_file(str(urihash), utils.get_cachedir(), json.dumps(retval))
            print retval
        else:
            print("Houston we have a problem, {}").format(retval)
    else:
        #TODO add async cache refresh
        print buf

#TODO Create higher abstraction for YANG Mounts
