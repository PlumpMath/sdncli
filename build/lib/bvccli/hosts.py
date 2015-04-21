from api import API
import requests
from pprint import pprint
from utils import print_table


def _get_bvc_hosts(ctl, debug=False):
    '''
    Get all hosts connected to known switches using topology data source
    '''
    resource = API['TOPOLOGY'].format(server=ctl.server)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return(("Error connecting to BVC {}").format(ctl.server), False)
    if str(retval.status_code)[:1] == "2":
        hosttable = {}
        data = retval.json()
        if debug:
            pprint.pprint(data)
        nodes = data.get('network-topology').get('topology')
        for node in nodes:
            topology_nodes = node.get('node')
            if topology_nodes is not None:
                for t_node in topology_nodes:
                    if 'host' in t_node.get('node-id'):
                        host = {'t_id': t_node.get('termination-point'),
                                'htsa': t_node.get('host-tracker-service:addresses')
                                }
                        hosttable.setdefault(t_node.get('node-id'), []).append(host)
                return(hosttable, True)
            else:
                return ("No hosts found", False)
    else:
        return (("Unexpected Status Code {}").format(retval.status_code), False)


def show_hosts(ctl, debug=False):
        dbhosts = {}
        (retval, status) = _get_bvc_hosts(ctl, debug)
        hosttable = retval
        if status:
            #TODO Check empty collection
            if hosttable is not None:
                for hosts in hosttable:
                    host = hosttable.get(hosts)
                    for h in host:
                        tid = h.get('t_id')
                        htsa = h.get('htsa')
                        for p in htsa:
                            for q in tid:
                                hostmap = {'IP': p.get('ip'), 'MacAddr': p.get('mac'), 'TID': q.get('tp-id')}
                                dbhosts.setdefault(p.get('id'), []).append(hostmap)
                if len(dbhosts) > 0:
                    print_table("get_hosts", dbhosts)
                else:
                    print "Found no Hosts"
                    return
            #TODO ?
            else:
                print "No hosts found"
                return None
        else:
            print("Error: {}").format(retval)
