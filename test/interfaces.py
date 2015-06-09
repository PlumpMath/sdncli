class Interface(object):
    def __init__(self, name, description, intftype, enabled, lude):
        self.name = name
        self.description = description
        self.type = intftype
        self.enabled = enabled
        self.linkupdowntrapenabled = lude


class Interfacestate(Interface):
    def __init__(self, admin, oper, lc, pa, hli, lli, speed):
        self.adminstatus = admin
        self.operstatus = oper
        self.last_change = lc
        self.phys_addr = pa
        self.higher_layer_if = hli
        self.lower_layer_if = lli
        self.speed = speed


class Statistics(object):
    def __init__(self, in_octets, in_unicast_pkts, in_broadcast_pkts, in_multicast_pkts, in_discards, in_errors, in_unknown_protos,
                 out_octets, out_unicast_pkts, out_broadcast_pkts, out_multicast_pkts, out_discards, out_errors):
        self.in_octets = in_octets
        self.in_unicast_pkta = in_unicast_pkts
        self.in_broadcast_pkts = in_broadcast_pkts
        self.in_multicast_pkts = in_multicast_pkts
        self.in_discards = in_discards
        self.in_errors = in_errors
        self.in_unknown_protos = in_unknown_protos
        self.out_octets = out_octets
        self.out_unicast_pkts = out_unicast_pkts
        self.out_broadcast_pkts = out_broadcast_pkts
        self.out_multicast_pkts = out_multicast_pkts
        self.out_discards = out_discards
        self.out_errors = out_errors

