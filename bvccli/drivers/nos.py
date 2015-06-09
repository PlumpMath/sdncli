
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
        # return netconf._netconf_delete(self.ctl, self.node, 'config', 'NETCONF', True, resource='/brocade-ras:logging/syslog-server/{}'.format(sysloghost))

    def get_syslog_host(self, sysloghost):
        pass
        # return netconf._netconf_get(self.ctl, self.node, 'config', 'NETCONF', True, resource='/brocade-ras:logging/syslog-server/{}'.format(sysloghost))

    def get_interfaces(self):
        resource = API['NOSINTERFACE'].format(server=self.ctl.server, node=self.node)
        try:
            retval = self.ctl.session.get(resource, auth=self.ctl.auth, params=None, headers=self.ctl.headers, timeout=120)
        except requests.exceptions.ConnectionError:
            raise requests.ConnectionError("Error Connecting to Server: {}".format(self.node))
        return retval
        # result = netconf._netconf_get(self.ctl, self.node, 'operational', 'NETCONF', True, resource='/brocade-interface:interface')
