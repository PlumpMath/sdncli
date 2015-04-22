from pprint import pprint
from ..common import api
from ..common import utils
import requests
from ascii_graph import Pyasciigraph


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
        graph = Pyasciigraph(graphsymbol='*')
        for l in graph.graph('Heap Usage', value.items()):
            print l


def system_get_gcinfo(ctl, args):
    (retval, status) = _system_get(ctl, 'GC', False)

    if status:
        value = retval['value']
        pprint(value)
        if 'java.lang:name=PS MarkSweep,type=GarbageCollector' in value.keys():
            print "Old Generation GC: PS MarkSweep"
            oldgen = value['java.lang:name=PS MarkSweep,type=GarbageCollector']
        if 'java.lang:name=MarkSweepCompact,type=GarbageCollector' in value.keys():
            print "Old Generation GC: MarkSweepCompact"
            oldgen = value['java.lang:name=MarkSweepCompact,type=GarbageCollector']
        if 'java.lang:name=ConcurrentMarkSweep,type=GarbageCollector' in value.keys():
            print "Old Generation GC: ConcurrentMarkSweep"
            oldgen = value['java.lang:name=ConcurrentMarkSweep,type=GarbageCollector']
        if 'java.lang:name=G1 Mixed Generation,type=GarbageCollector' in value.keys():
            print "Old Generation GC: G1 Mixed Generation"
            oldgen = value['java.lang:name=G1 Mixed Generation,type=GarbageCollector']
        if 'java.lang:name=PS Scavenge,type=GarbageCollector' in value.keys():
            print "Young Generation GC: PS Scavenge"
            newgen = value['java.lang:name=PS Scavenge,type=GarbageCollector']
        if 'java.lang:name=Copy,type=GarbageCollector' in value.keys():
            print "Young Generation GC: Copy"
            newgen = value['java.lang:name=Copy,type=GarbageCollector']
        if 'java.lang:name=ParNew,type=GarbageCollector' in value.keys():
            print "Young Generation GC: ParNew"
            newgen = value['java.lang:name=ParNew,type=GarbageCollector']
        if 'java.lang:name=G1 Young Generation,type=GarbageCollector' in value.keys():
            print "Young Generation GC: G1 Young Generation"
            newgen = value['java.lang:name=G1 Young Generation,type=GarbageCollector']

        before = newgen['LastGcInfo']['memoryUsageBeforeGc']
        after = newgen['LastGcInfo']['memoryUsageAfterGc']
        print "_______________________________________________________________________________"
        print "Before GC:"
        print "_______________________________________________________________________________"
        graph = Pyasciigraph(graphsymbol='.')
        for l in graph.graph('PS Eden Space', before['PS Eden Space'].items()):
            print l
        for l in graph.graph('PS Old Gen', before['PS Old Gen'].items()):
            print l
        for l in graph.graph('PS Survivor Space', before['PS Survivor Space'].items()):
            print l
        for l in graph.graph('PS Perm Gen', before['PS Perm Gen'].items()):
            print l
        for l in graph.graph('PS Survivor Space', before['PS Survivor Space'].items()):
            print l
        for l in graph.graph('Code Cache', before['Code Cache'].items()):
            print l 

        print "_______________________________________________________________________________"
        print "After GC:"
        print "_______________________________________________________________________________"
        graph = Pyasciigraph(graphsymbol='.')
        for l in graph.graph('PS Eden Space', after['PS Eden Space'].items()):
            print l
        for l in graph.graph('PS Old Gen', after['PS Old Gen'].items()):
            print l
        for l in graph.graph('PS Survivor Space', after['PS Survivor Space'].items()):
            print l
        for l in graph.graph('PS Perm Gen', after['PS Perm Gen'].items()):
            print l
        for l in graph.graph('PS Survivor Space', after['PS Survivor Space'].items()):
            print l
        for l in graph.graph('Code Cache', after['Code Cache'].items()):
            print l

      
       
