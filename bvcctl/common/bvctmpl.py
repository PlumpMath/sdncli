# addflow = {"flow":
#            [
#                {
#                    "id": flowid,
#                    "priority": priority,
#                    "table_id": tableid,
#                    "hard-timeout": htimeout,
#                    "idle-timeout": itimeout,
#                    "flow-name": flowname,
#                    "match": match,
#                    # {"ipv4-destination":"10.0.10.2/24",
#                    #  "ethernet-match":{"ethernet-type":{"type":2048}}
#                    # },
#                    "instructions":
#                    {"instruction":
#                        [{"order": order,
#                          "apply-actions":
#                            {"action": action
#                             # [{"order":0,
#                             #   "output-action":{"output-node-connector":"1"}
#                             # }]
#                             }
#                          }]
#                     }
#                    }
#                ]
#            }
