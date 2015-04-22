from __future__ import with_statement
from __future__ import unicode_literals
from pprint import pprint
from ..common import api
from ..common import utils
import requests
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *


def _system_get(ctl, apicall, debug, resource=None):
    resource = api.JMXAPI[apicall].format(server=ctl.server, resource=resource)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers,  timeout=120)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to BVC {}").format(ctl.server), False)
    if str(retval.status_code)[:1] == "2":
        try:
            data = retval.json()
            if debug:
                pprint(data)
        except ValueError, e:
            return(("Bad JSON found: {} {}").format(e, retval.text), False)
        return(data, True)
    else:
        return (("Unexpected Status Code {}").format(retval.status_code), False)


def system_get_heapinfo(ctl, args):
    (retval, status) = _system_get(ctl, 'HEAPUSAGE', False)
    if status:
        value = retval['value']
        utils.print_table_detail2('Heap', value)


def system_get_gcinfo(ctl, args):
    (retval, status) = _system_get(ctl, 'GC', False)

    if status:
        value = retval['value']
        if 'java.lang:name=PS MarkSweep,type=GarbageCollector' in value.keys():
            print "Using PS MarkSweep for Old Generation GC"
            oldgen = value['java.lang:name=PS MarkSweep,type=GarbageCollector']
        if 'java.lang:name=MarkSweepCompact,type=GarbageCollector' in value.keys():
            print "Using MarkSweepCompact for Old Generation GC"
            oldgen = value['java.lang:name=MarkSweepCompact,type=GarbageCollector']
        if 'java.lang:name=ConcurrentMarkSweep,type=GarbageCollector' in value.keys():
            print "Using ConcurrentMarkSweep for Old Generation GC"
            oldgen = value['java.lang:name=ConcurrentMarkSweep,type=GarbageCollector']
        if 'java.lang:name=G1 Mixed Generation,type=GarbageCollector' in value.keys():
            print "Using G1 Mixed Generation for Old Generation GC"
            oldgen = value['java.lang:name=G1 Mixed Generation,type=GarbageCollector']
        if 'java.lang:name=PS Scavenge,type=GarbageCollector' in value.keys():
            print "Using PS Scavenge for Young Generation GC"
            newgen = value['java.lang:name=PS Scavenge,type=GarbageCollector']
        if 'java.lang:name=Copy,type=GarbageCollector' in value.keys():
            print "Using Copy for Young Generation GC"
            newgen = value['java.lang:name=Copy,type=GarbageCollector']
        if 'java.lang:name=ParNew,type=GarbageCollector' in value.keys():
            print "Using ParNew for Young Generation GC"
            newgen = value['java.lang:name=ParNew,type=GarbageCollector']
        if 'java.lang:name=G1 Young Generation,type=GarbageCollector' in value.keys():
            print "Using G1 Young Generation for Young Generation GC"
            newgen = value['java.lang:name=G1 Young Generation,type=GarbageCollector']

        # # utils.print_table_detail2('Heap', newgen)
        # # oldgcinfo = oldgen['LastGcInfo']
        memuseaftergc = oldgen['LastGcInfo']['memoryUsageAfterGc']
        # memusebefgc = oldgen['LastGcInfo']['memoryUsageBeforeGc']
        # print "Old Generation"
        # print "Memory Before GC:"
        # for i in memusebefgc:
        #     utils.print_table_detail2(i, memusebefgc[i])
        # print "Memory After GC:"
        # for i in memuseaftergc:
        #     utils.print_table_detail2(i, memuseaftergc[i])

        # # newgcinfo = newgen['LastGcInfo']
        # memuseaftergc = newgen['LastGcInfo']['memoryUsageAfterGc']
        # memusebefgc = newgen['LastGcInfo']['memoryUsageBeforeGc']
        # print "Young Generation"
        # print "Memory Before GC:"
        # for i in memusebefgc:
        #     utils.print_table_detail2(i, memusebefgc[i])
        # print "Memory After GC:"
        # for i in memuseaftergc:
        #     utils.print_table_detail2(i, memuseaftergc[i])

        test = [('initial', 32560000), ('commited', 2225000), ('used', 0)]
        # for i in memuseaftergc:
        graph = Pyasciigraph(graphsymbol='*')
        for l in graph.graph('OldGen', test):
            print l
