from smd._internals import _Data, Index, Commands
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32


class SMDRed():
    _BROADCAST_ID = 0xFF
    _PRODUCT_TYPE = None
    _PACKAGE_ESSENTIAL_SIZE = 5

    def __init__(self, ID: int) -> None:

        self.__ack_size = 0
        self.vars = [
            _Data(Index.Header, 'B', False, 0x55),
            _Data(Index.DeviceID, 'B'),
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

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:4]])
        for index, value in zip(index_list, value_list):
            self.vars[int(index)].value(value)
            fmt_str += 'B' + self.vars[int(index)].type()

        self.__ack_size = struct.calcsize(fmt_str)

        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:4]], *[val for pair in zip(index_list, [self.vars[int(index)].value() for index in index_list]) for val in pair]]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def get_variables(self, index_list=[]):
        self.vars[Index.Command].value(Commands.READ)

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:4]])
        fmt_str += 'B' * len(index_list)

        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue()].type()) \
            + struct.calcsize(''.join(self.vars[idx].type() for idx in index_list))

        struct_out = list(*[var.value() for var in self.vars[:4]], *[int(idx) for idx in index_list])

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def reboot(self):
        pass

    def EEPROM_write(self):
        pass

    def ping(self):
        pass


class Master():
    def __init__(self) -> None:
        pass

    def __del__(self):
        pass

    def __write_bus(self):
        pass

    def __read_bus(self):
        pass

    def attach(self, ID):
        pass

    def detach(self, ID):
        pass

    def write(self, ID):
        pass

    def read(self, ID):
        pass

    def sync_write(self, IDs: list):
        pass

    def sync_read(self, IDs: list):
        pass

    def bulk_write(self, IDs: list):
        pass

    def bulk_read(self, IDs: list):
        pass

    def reboot(self, IDs: list):
        pass
