import json


def get_cliconf_devices(ctl):
    template_url = "http://{}:{}/restconf/config/cliconf:devices".format(ctl.ipAddr, ctl.portNum)
    response = ctl.http_get_request(template_url, data=None, headers=None)
    if(response.status_code == 200):
        return json.loads(response.content)
    else:
        return None

# class Statistics(object):
#     def __init__(self, in_octets, in_unicast_pkts, in_broadcast_pkts, in_multicast_pkts, in_discards, in_errors, in_unknown_protos,
#                  out_octets, out_unicast_pkts, out_broadcast_pkts, out_multicast_pkts, out_discards, out_errors):
#         self.in_octets = in_octets
#         self.in_unicast_pkta = in_unicast_pkts
#         self.in_broadcast_pkts = in_broadcast_pkts
#         self.in_multicast_pkts = in_multicast_pkts
#         self.in_discards = in_discards
#         self.in_errors = in_errors
#         self.in_unknown_protos = in_unknown_protos
#         self.out_octets = out_octets
#         self.out_unicast_pkts = out_unicast_pkts
#         self.out_broadcast_pkts = out_broadcast_pkts
#         self.out_multicast_pkts = out_multicast_pkts
#         self.out_discards = out_discards
#         self.out_errors = out_errors


# class Interface(object):
#     def __init__(self, name, description, intftype, enabled, lude):
#         self.name = name
#         self.description = description
#         self.type = intftype
#         self.enabled = enabled
#         self.linkupdowntrapenabled = lude
#         self.interfacestate = Interfacestate()
#         self.statistics = Statistics()
