from ncclient import manager
import pprint

host="10.255.1.212"


# with manager.connect(host=host) as m:
#     c = m.get_config(source="running").data_xml
#     pprint.pprint(c)

# with manager.connect(host=host, port=830, username="admin", password="admin", hostkey_verify=False) as m:
#     c = m.get_config(source="running").data_xml
#     pprint.pprint(c)

with manager.connect_ssh(host=host, port=830, username="admin", hostkey_verify=False, allow_agent=True, look_for_keys=False) as m:
    c = m.get_config(source="running").data_xml
    pprint.pprint(c)


