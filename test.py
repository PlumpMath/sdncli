table = {}

table = {'host:00:00:00:00:00:01': [{'htsa': [{'first-seen': 1425650760295, 'id': 18, 'ip': '10.0.0.1',
                                     'last-seen': 1425672225570, 'mac': '00:00:00:00:00:01'}], 't_id': [{'tp-id': 'host:00:00:00:00:00:01:openflow:1:1'}]}]}
table1 = {'host:00:00:00:00:00:01': {'htsa': [{'first-seen': 1425650760295, 'id': 18, 'ip': '10.0.0.1'}]}}
                                     

table2 = [{u'host:00:00:00:00:00:01': [{'htsa': [{u'first-seen': 1425650760295,
                                        u'id': 18,
                                        u'ip': u'10.0.0.1',
                                        u'last-seen': 1425672225570,
                                        u'mac': u'00:00:00:00:00:01'}],
                              't_id': [{u'tp-id': u'host:00:00:00:00:00:01:openflow:1:1'}]}],
 u'host:00:00:00:00:00:02': [{'htsa': [{u'first-seen': 1425650765308,
                                        u'id': 20,
                                        u'ip': u'10.0.0.2',
                                        u'last-seen': 1425672225570,
                                        u'mac': u'00:00:00:00:00:02'}],
                              't_id': [{u'tp-id': u'host:00:00:00:00:00:02:openflow:2:1'}]}],
 u'host:00:00:00:00:00:03': [{'htsa': [{u'first-seen': 1425650765294,
                                        u'id': 19,
                                        u'ip': u'10.0.0.3',
                                        u'last-seen': 1425672225587,
                                        u'mac': u'00:00:00:00:00:03'}],
                              't_id': [{u'tp-id': u'host:00:00:00:00:00:03:openflow:3:1'}]}]}]


def recv_tbl(table):
    for entry in table:
        #strip list
        for host in entry:
            #host list
            #get key
            a = entry.get(host)
            #first list (t_id and Htsa)
            for hostlist in a:
                #get dict htsa
                htsa = hostlist.get('htsa')
                tid = hostlist.get('t_id')
                for p in htsa:
                    print p.get('ip')
                    print p.get('id')
                    print p.get('mac')
                for q in tid:
                    print q.get('tp-id')



    # l = table.get('host:00:00:00:00:00:01')
    # m = l.get('htsa')
    # print l, m
    # for n in m:
    #     print n.get('ip')

def send_tbl():
    recv_tbl(table2)



send_tbl()