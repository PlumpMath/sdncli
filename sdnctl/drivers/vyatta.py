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

    def maptoietfinterfaces(self, data):
        ilist = []
        for iface in data['interfaces']['vyatta-interfaces-dataplane:dataplane']:
            if iface is not None:
                ilist.append({'node': self.node, 'name': iface['tagnode'], 'description': iface.get('description', 'none'),
                              'mtu': iface.get('mtu', 'unknown'), 'enabled': 'fixme', 'type': 'dataplane', 'vlan': iface.get('vlan', 'none'),
                              'address': iface.get('address', 'none')})
                if 'vif' in iface:
                    for vif in iface['vif']:
                        if vif is not None:
                            if 'disable' in vif:
                                enabled = False
                            else:
                                enabled = True
                            ilist.append({'node': self.node, 'name': "{}.{}".format(iface['tagnode'], vif['tagnode']), 'description': vif.get('description', 'none'),
                                          'mtu': vif.get('mtu', 'unknown'), 'enabled': enabled, 'type': 'vif', 'vlan': vif.get('vlan', 'none'),
                                          'address': vif.get('address', 'none')})

                return ilist
