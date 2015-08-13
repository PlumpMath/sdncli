
# from ..netconf import netconf
from ..httplib import httplib as h
from ..common.api import API
import requests


class NOS(object):
    def __init__(self, ctl, node):
        self.node = node
        self.ctl = ctl

    def set_syslog_host(self, sysloghost, facility="all", level="warning", port=514):
        syslog = {"system": {"syslog-server": [{"syslogip": sysloghost, "port": port}]}}
        # return netconf._netconf_post(self.ctl, self.node, 'config', 'NETCONF', True, resource='/brocade-ras:logging', payload=json.dumps(syslog))

    def delete_syslog_host(self, sysloghost, facility="all", level="warning", port=None):
        pass

    def get_syslog_host(self, sysloghost):
        pass

    def get_interfaces(self):
        resource = API['NOSINTERFACE'].format(server=self.ctl.server, node=self.node)
        print resource
        try:
            retval = self.ctl.session.get(resource, auth=self.ctl.auth, params=None, headers=self.ctl.headers, timeout=240)
        except requests.exceptions.ConnectionError:
            raise requests.ConnectionError("Error Connecting to Server: {}".format(self.node))
        return retval

    def maptoietfinterfaces(self, data):
        ilist = []
        for i in data['interface']:
            if i is not None:
                d = data['interface'][i]
                for iface in d:
                    if iface.get('shutdown') is None:
                        enabled = 'true'
                    else:
                        enabled = 'false'

                    ilist.append({'node': self.node, 'name': iface['name'], 'description': iface.get('description', 'none'),
                                  'mtu': iface.get('mtu', 'unknown'), 'enabled': enabled, 'type': i, 'vlan': iface.get('vlan', 'none'),
                                  'address': iface.get('address', 'none')})

                return ilist
