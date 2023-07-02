import struct
import enum


class Commands(enum.IntEnum):
    PING = 0x00,
    READ = 0x01,
    WRITE = 0x02,
    REBOOT = 0x05,
    EEPROM_WRITE = 0x03,
    BL_JUMP = 0x30,
    __SYNC_WRITE = -1
    __BULK_WRITE = -1
    __BULK_READ = -1
    __ACK = -1,
    __WRITE_ACK = 1
    __EEPROM_WRITE_ACK = -1


Index = enum.IntEnum('Index', [
    'Header',
    'DeviceID',
    'PackageSize',
    'Command',
    'Error',
    'Baudrate',
    'OperationMode',
    'CRCValue',
    ], start=0)


class _Data():
    def __init__(self, index, var_type, rw=True, value=0):
        self.__index = index
        self.__type = var_type
        self.__size = struct.calcsize(self.__type)
        self.__value = value
        self.__rw = rw

    def value(self, value=None):
        if value is None:
            return self.__value
        elif self.__rw:
            self.__value = struct.unpack('<' + self.__type, struct.pack('<' + self.__type, value))[0]

    def index(self) -> enum.IntEnum:
        return self.__index

    def size(self) -> int:
        return self.__size

    def type(self) -> str:
        return self.__type
