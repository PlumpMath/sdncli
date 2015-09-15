from pybvc.common.result import Result
from pybvc.common.status import OperStatus, STATUS
import json


class Cisco(object):
    def __init__(self):
        return

    @staticmethod
    def get_interfaces_cfg(ctrl, name):
            """ Return the configuration for the interfaces on the VRouter5600
            :return: A tuple: Status, configuration of the interfaces
            :rtype: instance of the `Result` class (containing configuration data)
            - STATUS.CONN_ERROR: If the controller did not respond.
            - STATUS.CTRL_INTERNAL_ERROR: If the controller responded but did not
                                          provide any status.
            - STATUS.OK:  Success. Result is valid.
            - STATUS.HTTP_ERROR: If the controller responded with an error
                                 status code.
            """
            status = OperStatus()
            cfg = None
            templateModelRef = "cisco-9k:interfaces"
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
        for i in data['interfaces']['interface']:
            ilist.append({'node': node,
                          'name': i['name'],
                          'mtu': i.get('mtu', 'unknown'),
                          'operstatus': i.get('operstatus', 'unknown'),
                          'adminstatus': i.get('adminstatus', 'unknown'),
                          'ipv4-address': i.get('ipv4-address', 'unknown'),
                          'mac': i.get('mac', 'unknown')})
        return ilist
