"""
Usage:
        sdncli system [options] nonheap
        sdncli system [options] heap
        sdncli system [options] gc

Options :
            -d --debug             Print JSON dump
            -v --verbose           Add verbose output
            -h --help              This help screen

"""

from pprint import pprint
from ..common import api
import requests
from ascii_graph import Pyasciigraph


def _system_get(ctl, apicall, debug=True, resource=None):
    resource = api.JMXAPI[apicall].format(server=ctl.server, resource=resource)
    try:
        retval = ctl.session.get(resource, auth=ctl.auth, params=None, headers=ctl.headers,  timeout=120)
    except requests.exceptions.ConnectionError:
        return (("Error connecting to Controller {}").format(ctl.server), False)
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
        graph = Pyasciigraph(graphsymbol='.')
        for l in graph.graph('Heap Memory Usage', value.items()):
            print l


def system_get_nonheap(ctl, args):
    (retval, status) = _system_get(ctl, 'NONHEAP', False)
    if status:
        value = retval['value']
        graph = Pyasciigraph(graphsymbol='.')
        for l in graph.graph('Non-Heap Memory Usage', value.items()):
            print l


def mem_banner():
    print """
init        represents the initial amount of memory (in bytes) that the Java virtual machine requests from the operating system for memory management during startup. 
            The Java virtual machine may request additional memory from the operating system and may also release memory to the system over time. The value of init 
            may be undefined.
used        represents the amount of memory currently used (in bytes).
committed   represents the amount of memory (in bytes) that is guaranteed to be available for use by the Java virtual machine. The amount of committed memory may 
            change over time (increase or decrease). The Java virtual machine may release memory to the system and committed could be less than init. committed 
            will always be greater than or equal to used.
max         represents the maximum amount of memory (in bytes) that can be used for memory management. Its value may be undefined. The maximum amount of memory may 
            change over time if defined. The amount of used and committed memory will always be less than or equal to max if max is defined. A memory allocation 
            may fail if it attempts to increase the used memory such that used > committed even if used <= max would still be true (for example, when the system is 
            low on virtual memory).
"""


def system_get_gcinfo(ctl, args):
    (retval, status) = _system_get(ctl, 'GC', False)
    pprint(retval)
    if status:
        value = retval['value']
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
        for k in before.keys():
            for l in graph.graph(k, before[k].items()):
                print l
        print "_______________________________________________________________________________"
        print "After GC:"
        print "_______________________________________________________________________________"
        graph = Pyasciigraph(graphsymbol='.')
        for k in after.keys():
            for l in graph.graph(k, after[k].items()):
                print l
        print "_______________________________________________________________________________"
        mem_banner()
