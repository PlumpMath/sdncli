import json


def send_notify(ctl, ds, scope):

    payload = {"input": {
               "path": "opendaylight-inventory:nodes",
               "datastore": ds,
               "scope": scope}
               }

    json.loads(payload)
    