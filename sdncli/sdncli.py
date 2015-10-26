"""Copyright (c) 2015

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
-  Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
-  Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
-  Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES;LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

doc = """
Brocade SDN Controller - Command Line Interface
Brocade Communications, Inc.

Usage:
        sdncli [options] <command> [<args>...]

Options :
            -a --address <ip>      Address of controller (default: localhost)
            -d --debug             Print JSON dump
            -h --help              This help screen

Commands:
             flow      Perform OpenFlow functions
             show          Retrieve varios elements from BVC
             node          Perform Node related functions such as retrieve configuration
             http          Perform HTTP based operations

"""

from docopt import docopt
from pybvc.controller.controller import Controller
from pybvc.common.status import STATUS

from requests import ConnectionError
from exceptions import AttributeError

import lib.show
import lib.node
import lib.flow
import lib.http
import lib.interface


# from logging import log
# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# logging.propagate = True
# requests_log = logging.getLogger("requests")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class Session(Controller):
    def __init__(self, ip, port, user, password):
        Controller.__init__(self, ip, port, user, password)
        # initialize session object
        result = self.build_inventory_object()
        if(result.status.eq(STATUS.OK)):
            self.inventory = result.data
            result = self.build_topology_object("flow:1")
            if(result.status.eq(STATUS.OK)):
                self.topology = result.data
            else:
                print "Warning: Can't build topology"
        else:
            print "Houston we have a problem {}".format(result.status.to_string())
            exit()


def main():
    import pdb
    port = '8181'
    auth = {'user': 'admin', 'password': 'admin'}
    args = docopt(doc, options_first=True)

    cmd = args['<command>']
    subcmd = args['<args>']
    commands = [cmd] + subcmd

    try:
        if args.get('--address') is not None:
            ctl = Session(args['--address'], port, auth.get('user', 'admin'), auth.get('password', 'admin'))
        else:
            ctl = Session('127.0.0.1', port, auth.get('user', 'admin'), auth.get('password', 'admin'))
    except ConnectionError, e:
        print("Can't establish connection to controller {}".format(args.get('--address')))
        exit()

    try:
        module = getattr(lib, cmd)
    except AttributeError, e:
        raise e
    arguments = docopt(module.__doc__, commands)
    try:
        # pass
        pdb.set_trace()
        getattr(module, cmd)(ctl, arguments)
    except Exception, e:
        raise e

if __name__ == '__main__':
        main()
