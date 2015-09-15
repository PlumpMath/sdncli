"""
Usage:
        sdncli flow delete <node> <table> <flow>

Options :
            -h --help              This help screen
            -o --operations        Read from operations datastore
            -c --config            Read from configuration datastore

"""
from pybvc.common.status import STATUS
from pybvc.openflowdev.ofswitch import OFSwitch

# from pybvc.controller.topology import Topology


def flow(ctl, args):
    # DELETE
    if args.get('delete'):
        node = args['<node>']
        tid = args['<table>']
        fid = args['<flow>']
        ofswitch = OFSwitch(ctl, node)
        result = ofswitch.delete_flow(tid, fid)
        if(result.status.eq(STATUS.OK)):
            print "Successfully deleted flow {}:{}:{}".format(node, tid, fid)
        # TODO Status codes for immutable calls are wrong.
        elif(result.status_code == 10):
            print "Flow already exists"
        else:
            print "Houston we have a problem!"
