from smd._internals import _Data, Index, Commands
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import serial
import time


class SMDRed():
    _BROADCAST_ID = 0xFF
    _PRODUCT_TYPE = 0xBA
    _PACKAGE_ESSENTIAL_SIZE = 6

    def __init__(self, ID: int) -> bool:

        self.__ack_size = 0
        self.vars = [
            _Data(Index.Header, 'B', False, 0x55),
            _Data(Index.DeviceID, 'B'),
            _Data(Index.DeviceFamily, 'B', False, self.__class__._PRODUCT_TYPE),
            _Data(Index.PackageSize, 'B'),
            _Data(Index.Command, 'B'),
            _Data(Index.Status, 'B'),
            _Data(Index.Baudrate, 'I'),
            _Data(Index.OperationMode, 'B'),
            _Data(Index.CRCValue, 'I'),
        ]

        if ID > 255 or ID < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        else:
            self.vars[Index.DeviceID].value(ID)

    def get_ack_size(self):
        return self.__ack_size

    def set_variables(self, index_list=[], value_list=[], ack=False):
        self.vars[Index.Command].value(Commands.__WRITE_ACK if ack else Commands.WRITE)

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        for index, value in zip(index_list, value_list):
            self.vars[int(index)].value(value)
            fmt_str += 'B' + self.vars[int(index)].type()

        self.__ack_size = struct.calcsize(fmt_str)

        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:5]], *[val for pair in zip(index_list, [self.vars[int(index)].value() for index in index_list]) for val in pair]]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def get_variables(self, index_list=[]):
        self.vars[Index.Command].value(Commands.READ)

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        fmt_str += 'B' * len(index_list)

        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue()].type()) \
            + struct.calcsize(''.join(self.vars[idx].type() for idx in index_list))

        struct_out = list(*[var.value() for var in self.vars[:4]], *[int(idx) for idx in index_list])

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def reboot(self):
        self.vars[Index.Command].value(Commands.REBOOT)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = struct.pack(fmt_str, list(*[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = 0
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def EEPROM_write(self, ack=False):
        self.vars[Index.Command].value(Commands.__EEPROM_WRITE_ACK if ack else Commands.EEPROM_WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = struct.pack(fmt_str, list(*[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def ping(self):
        self.vars[Index.Command].value(Commands.PING)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = struct.pack(fmt_str, list(*[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def change_id(self, id):
        self.vars[Index.Command].value(Commands.WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:5]], [id]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

class Master():
    def __init__(self, portname, baudrate=115200) -> None:
        self.__driver_list = [SMDRed(255)] * 256
        if baudrate > 6250000 or baudrate < 1537:
            raise ValueError('Baudrate must be in range of 1537 to 6.25M')
        else:
            self.__baudrate = baudrate
            self.__post_sleep = 10 / self.__baudrate
            self.__ph = serial.Serial(port=portname, baudrate=self.__baudrate, timeout=0.1)

    def __del__(self):
        try:
            self.__ph.close()
        except:
            pass

    def __write_bus(self, data):
        self.__ph.write(data)

    def __read_bus(self, size) -> bytes:
        self.__ph.reset_input_buffer()
        return self.read(size=size)

    def update_baudrate(self, baud: int):
        self.__ph.reset_input_buffer()
        self.__ph.reset_output_buffer()

        try:
            self.__ph.baudrate(baud)
        except:
            pass

    def attach(self, driver: SMDRed):
        self.__driver_list[driver.vars[Index.DeviceID].value()] = driver

    def detach(self, id):
        self.__driver_list[id] = SMDRed(255)

    def parse(self, data):
        id = data[Index.DeviceID]
        data = data[5:-4]
        fmt_str = '<'

        i = 0
        while i < len(data):
            fmt_str += 'B' + self.__driver_list[id].vars[data[i]].type()
            i += self.__driver_list[id].vars[data[i]].size() + 1

        unpacked = list(struct.unpack(fmt_str, data))
        grouped = zip(*[iter(unpacked)] * 2, strict=True)

        for group in grouped:
            self.__driver_list[id].vars[group[0]].value(group[1])

    def __read_ack(self, id) -> bool:
        ret = self.__read_bus(self.__driver_list[id].get_ack_size())
        if len(ret) == self.__driver_list[id].get_ack_size():
            if CRC32.calc(ret[:-4]) == struct.unpack('<I', ret[-4:])[0]:
                if ret[int(Index.PackageSize)] > 9:
                    self.parse(ret)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def sync_write(self, id):
        raise NotImplementedError()

    def sync_read(self, id):
        raise NotImplementedError()

    def bulk_write(self, id):
        raise NotImplementedError()

    def bulk_read(self, id):
        raise NotImplementedError()

    def reboot(self, id):
        self.__write_bus(self.__driver_list[id].reboot())
        time.sleep(self.__post_sleep)

    def eeprom_write(self, id, ack=False):
        self.__write_bus(self.__driver_list[id].EEPROM_write(ack=ack))
        time.sleep(self.__post_sleep)

        if ack:
            if self.__read_ack(id):
                return True
            else:
                return False

    def ping(self, id):
        self.__write_bus(self.__driver_list[id].ping())
        time.sleep(self.__post_sleep)

        if self.__read_ack(id):
            return True
        else:
            return False

    def scan(self) -> list:
        connected = []

        for idx in range(255):
            if self.ping(idx):
                connected.append(idx)
                self.attach((SMDRed(idx)))

        return connected
