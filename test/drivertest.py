import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(__file__+"/../.."))
from bvccli.common.controller import Controller
from bvccli.common.api import API


from pprint import pprint

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

from singledispatch import singledispatch
from bvccli.drivers.nos import NOS
from bvccli.drivers.vyatta import Vyatta5600


@singledispatch
def get_interfaces():
    raise NotImplementedError("Not Implemented Yet!")


@get_interfaces.register(NOS)
def _(obj):
    result = NOS.get_interfaces(obj)
    return result


@get_interfaces.register(Vyatta5600)
def _(obj):
    result = Vyatta5600.get_interfaces(obj)
    return result


def load_json_config():
    import json
    source = '''
        {"username": "admin",
         "password": "admin",
         "server": "madmax",
         "port": "8181"}
    '''
    return json.loads(source)

auth = load_json_config()


class TestNOS(unittest.TestCase):
    def test_NOS_interface(self):
        ctl = Controller(auth, 'madmax')
        vdx3 = NOS(ctl, 'vdx3')
        retval = vdx3.get_interfaces()
        self.assertTrue(retval.status_code, 200)
        # pprint(retval.json())


class TestVR(unittest.TestCase):
    def test_VR_interface(self):
        ctl = Controller(auth, 'madmax')
        vr = Vyatta5600(ctl, 'vr5600')
        retval = vr.get_interfaces()
        self.assertTrue(retval.status_code, 200)
        # pprint(retval.json())


class TestGenericInterface(unittest.TestCase):
    def test_generic_NOS_interfaces(self):
        ctl = Controller(auth, 'madmax')
        nos = NOS(ctl, 'vdx3')
        retval = get_interfaces(nos)
        self.assertTrue(retval.status_code, 200)

    def test_generic_VR_interfaces(self):
        ctl = Controller(auth, 'madmax')
        vr = Vyatta5600(ctl, 'vr5600')
        retval = get_interfaces(vr)
        self.assertTrue(retval.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=3)
