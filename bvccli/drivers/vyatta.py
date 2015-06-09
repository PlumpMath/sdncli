import requests
from ..netconf import netconf
import json
from ..httplib import httplib as h
from ..common.api import API


class Vyatta5600(object):
    def __init__(self, ctl, node):
        self.node = node
        self.ctl = ctl

    def set_syslog_host(self, sysloghost, facility="all", level="warning", port=None):
        syslog = {"vyatta-system:system": {"vyatta-system-syslog:syslog": {"host": [{"tagnode": sysloghost,
                                                                           "facility": [{"tagnode": facility}]}]}}}
        return netconf._netconf_post(self.ctl, self.node, 'config', 'NETCONF', False, payload=json.dumps(syslog))

    def delete_syslog_host(self, sysloghost, facility="all", level="warning", port=None):
        return netconf._netconf_delete(self.ctl, self.node, 'config', 'NETCONF', False, resource='/vyatta-system:system/vyatta-system-syslog:syslog/host/{}'.format(sysloghost))

    def get_syslog_host(self, sysloghost):
        return netconf._netconf_get(self.ctl, self.node, 'config', 'NETCONF', False, resource='/vyatta-system:system/vyatta-system-syslog:syslog/host/{}'.format(sysloghost))

    def get_interfaces(self):
        resource = API['VRINTERFACE'].format(server=self.ctl.server, node=self.node)
        try:
            retval = self.ctl.session.get(resource, auth=self.ctl.auth, params=None, headers=self.ctl.headers, timeout=120)
        except requests.exceptions.ConnectionError:
            raise requests.ConnectionError("Error Connecting to Server: {}".format(self.node))
        return retval
