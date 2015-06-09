
import unittest
import sys
import os
from pprint import pprint
sys.path.insert(0, os.path.abspath(__file__+"/../.."))

from bvccli.drivers.vyatta5600 import Vyatta5600
from bvccli.drivers.nos import NOS
from bvccli.core import Controller
from bvccli.common import utils


class TestAddSyslogVr5600(unittest.TestCase):
        auth = utils.load_json_config()
        ctl = Controller(auth, '192.168.59.103')
        vr = Vyatta5600(ctl, 'vr5600')

        def test_add_syslog_vr5600(self):
            #delete first
            self.vr.delete_syslog_host('172.16.44.116')
            self.status = self.vr.set_syslog_host('172.16.44.116')
            self.assertEqual(self.status.status_code, 204)
            #cleanup
            self.vr.delete_syslog_host('172.16.44.116')

        def test_get_syslog_vr5600(self):
            self.vr.set_syslog_host('172.16.44.116')
            status = self.vr.get_syslog_host('172.16.44.116')
            self.assertEqual(status.status_code, 200)

        def test_delete_syslog_vr5600(self):
            #add first
            self.vr.set_syslog_host('172.16.44.116')
            status = self.vr.delete_syslog_host('172.16.44.116')
            self.assertEqual(status.status_code, 200)


class TestAddSyslogNOS(unittest.TestCase):
        auth = utils.load_json_config()
        ctl = Controller(auth, '192.168.59.103')
        vdx = NOS(ctl, 'vdx2')

        def test_add_syslog(self):
            #delete first
            self.vdx.delete_syslog_host('172.16.40.119')
            self.status = self.vdx.set_syslog_host('172.16.40.119')
            self.assertEqual(self.status.status_code, 204)
            #cleanup
            self.vdx.delete_syslog_host('172.16.40.119')

        def test_get_syslog(self):
            self.vdx.set_syslog_host('172.16.40.119')
            status = self.vdx.get_syslog_host('172.16.40.119')
            pprint(status)
            self.assertEqual(status.status_code, 200)

        def test_delete_syslog(self):
            #add first
            self.vdx.set_syslog_host('172.16.40.119')
            status = self.vdx.delete_syslog_host('172.16.40.119')
            self.assertEqual(status.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=3)
