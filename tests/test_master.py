import unittest
from unittest.mock import patch
from smd import smd
from smd.types import CircularBuffer


class TestMaster(unittest.TestCase):

    def setUp(self) -> None:
        patcher = patch("smd.actuator.serial.Serial", autospec=True)
        self.mock = patcher.start()
        self.addCleanup(patcher.stop)
        self.mst = smd.Master(size=4096, portname='/dev/ttyUSB0', baudrate=115200)
        self.mock.reset_mock()

    def tearDown(self) -> None:
        pass

    def test_add_actuator(self):
        self.assertRaises(ValueError, self.mst.addActuator(-1))
        self.assertRaises(ValueError, self.mst.addActuator(256))

        ID = 1
        self.mst.addActuator(ID)
        self.assertTrue(ID in self.mst.ActList)

    def test_remove_actuator(self):
        self.assertRaises(ValueError, self.mst.addActuator(-1))
        self.assertRaises(ValueError, self.mst.addActuator(256))

        ID = 1
        self.mst.addActuator(ID)
        self.assertTrue(ID in self.mst.ActList)
        self.mst.removeActuator(ID)
        self.assertTrue(ID not in self.mst.ActList)

    def test_send(self):
        with patch.object(smd.Master, 'send') as wr:
            self.mst.send(bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4]))
            wr.assert_called_with(bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4]))

    def test_receive(self):
        self.mock.return_value.read.return_value = bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4])
        self.assertEqual([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4], self.mst.receive())

        self.mock.return_value.read.return_value = bytes([])
        self.assertEqual([], self.mst.receive())

    def test_find_package(self):
        with patch.object(smd.SMDRed, 'parse') as parse:
            self.mst.pass2buffer([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4])
            self.mst.findPackage()
            parse.assert_called_once()

    def test_auto_scan(self):
        self.mock.return_value.read.return_value = bytes([0x55, 0x00, 0x09, 0x00, 0x00, 0x7F, 0x9A, 0xEC, 0xA4])
        self.assertEqual([0], self.mst.AutoScan())
