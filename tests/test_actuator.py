import unittest
import unittest.mock
from unittest.mock import patch
from smd import actuator


class TestActuator(unittest.TestCase):
    def setUp(self):
        self.dev = actuator.Actuator(0)

    def tearDown(self):
        pass

    def test_ping(self):
        pkg_ping = bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4])

        ret = self.dev.Ping()
        self.assertEqual(ret, pkg_ping)

    def test_reboot(self):
        pkg_reboot = bytes([0x55, 0x00, 0x09, 0x05, 0x00, 0x0A, 0x7A, 0xD1, 0x33])

        ret = self.dev.Reboot()
        self.assertEqual(ret, pkg_reboot)

    def test_factory_reset(self):
        pkg_rst = bytes([0x55, 0x00, 0x09, 0x17, 0x00, 0x16, 0x7F, 0x72, 0x83])

        ret = self.dev.FactoryReset()
        self.assertEqual(ret, pkg_rst)

    def test_error_clear(self):
        pkg_err_clr = bytes([0x55, 0x00, 0x09, 0x18, 0x00, 0x3E, 0x42, 0xF5, 0x3E])

        ret = self.dev.ErrorClear()
        self.assertEqual(ret, pkg_err_clr)

    def test_eeprom_write(self):
        pkg_eeprom_wr = bytes([0x55, 0x00, 0x09, 0x03, 0x00, 0xAC, 0xC5, 0x07, 0xD6])

        ret = self.dev.ROMWrite()
        self.assertEqual(ret, pkg_eeprom_wr)

    @unittest.skip
    def test_write(self):
        pass

    @unittest.skip
    def test_read(self):
        pass