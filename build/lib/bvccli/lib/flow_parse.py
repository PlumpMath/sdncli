class Flowparse(object):
	pass


class MatchRules(object):

    match_types = ["ipv4-destination", "ethernet-match", "ethernet-type"]

    "match": match,
                   # {"ipv4-destination":"10.0.10.2/24",
                   #  "ethernet-match":{"ethernet-type":{"type":2048}}
                   # },
    return dict

# L2 : Port, Source MAC, Destination MAC, Ether type, Vlan, Vlan PCP
# L3 : Port, Vlan, Vlan PCP, Ethertype(IP,ARP,LLDP), Source IP, Destination IP, IP Protocol, IP TOS, IP Src Port, IP Dst Port
# L23: All


class Actions(object):

    action_instructions = ["output-action"]
    action_types = ["output-node-connector"]


    # [{"order":0,
                            #   "output-action":{"output-node-connector":"1"}
                            # }]

    return list
