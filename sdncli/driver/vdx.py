from pysdn.common.result import Result
from pysdn.common.status import OperStatus, STATUS


class NOS(object):
    def __init__(self):
        return

    @staticmethod
    def get_interfaces_cfg(ctrl, name):
            status = OperStatus()
            cfg = None
            templateModelRef = "brocade-interface:interface"
            modelref = templateModelRef
            url = ctrl.get_ext_mount_config_url(name)
            url += modelref
            resp = ctrl.http_get_request(url, data=None, headers=None, timeout=120)
            if(resp is None):
                status.set_status(STATUS.CONN_ERROR)
            elif(resp.content is None):
                status.set_status(STATUS.CTRL_INTERNAL_ERROR)
            elif (resp.status_code == 200):
                cfg = resp.content
                status.set_status(STATUS.OK)
            else:
                status.set_status(STATUS.HTTP_ERROR, resp)
            return Result(status, cfg)

    @staticmethod
    def maptoietfinterfaces(node, data):
        ilist = []
        for i in data['opinterfaces']['interface']:
            ilist.append({'node': node,
                          'name': i['name'],
                          'mtu': i.get('mtu', 'unknown'),
                          'operstatus': i.get('operstatus', 'unknown'),
                          'adminstatus': i.get('adminstatus', 'unknown'),
                          'ipv4-address': i.get('ipv4-address', 'unknown'),
                          'mac': i.get('mac', 'unknown')})
        return ilist
