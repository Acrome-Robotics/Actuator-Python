import unittest
import unittest.mock
from unittest.mock import patch
from smd import actuator


class TestActuator(unittest.TestCase):
    def setUp(self):
        self.dev = actuator.Actuator(0)

    def tearDown(self):
        pass

    def test_populate_header(self):
        header = bytes([0x55, 0x00, 0x15, 0x0, 0x03])

        ret = self.dev.__populate_header()
        self.assertEqual(ret, header)
        pass

    def test_calculate_crc(self):
        data = bytes([0x55, 0x00, 0x09, 0x00, 0x00])
        crc = bytes([0x7F, 0x9A, 0xEC, 0xA4])

        ret = self.dev.__calculate_crc(data)
        self.assertEqual(ret, crc)

    def test_ping(self):
        pkg_ping = bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4])

        ret = self.dev.Ping()
        self.assertListEqual(ret, pkg_ping)

    def test_reboot(self):
        pkg_reboot = bytes([0x55, 0x00, 0x09, 0x05, 0x00, 0xA0, 0x7A, 0xD1, 0x33])

        ret = self.dev.Reboot()
        self.assertListEqual(ret, pkg_reboot)

    def test_factory_reset(self):
        pkg_rst = bytes([0x55, 0x00, 0x09, 0x17, 0x00, 0x16, 0x7F, 0x72, 0x83])

        ret = self.dev.FactoryReset()
        self.assertListEqual(ret, pkg_rst)

    def test_rom_write(self):
        pkg_rom_wr = bytes([0x55, 0x00, 0x09, 0x03, 0x00, 0xAC, 0xC5, 0x70, 0xD6])

        ret = self.dev.ROMWrite()
        self.assertListEqual(ret, pkg_rom_wr)

    @unittest.skip
    def test_write(self):
        pass

    @unittest.skip
    def test_read(self):
        pass