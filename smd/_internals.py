import struct
import enum


class FamilyType():  # Specify Red, Blue and Green types
    pass


class Commands(enum.IntEnum):
    PING = 0x00,
    WRITE = 0x01,
    READ = 0x02,
    EEPROM_WRITE = 0x03,
    SCAN_SENSORS = 0x04
    REBOOT = 0x05,
    RESET_ENC = 0x06
    BL_JUMP = 0x30,
    SYNC_WRITE = 0x40 | 0x01
    BULK_WRITE = 0x20 | 0x01
    BULK_READ = 0x20 | 0x02
    ACK = 0x80,
    WRITE_ACK = 0x80 | 0x01
    __EEPROM_WRITE_ACK = -1


Index = enum.IntEnum('Index', [
    'Header',
    'DeviceID',
    'DeviceFamily',
    'PackageSize',
    'Command',
    'Status',
    'HardwareVersion',
    'SoftwareVersion',
    'Baudrate',
    'OperationMode',
    'TorqueEnable',
    'AutotunerEnable',
    'AutotuneMethod',
    'MotorCPR',
    'MotorRPM',
    'PWMFrequency',
    'SetDutyCycle',
    'MinimumPosition',
    'MaximumPosition',
    'TorqueLimit',
    'VelocityLimit',
    'PositionFF',
    'VelocityFF',
    'TorqueFF',
    'PosScalerGain',
    'PosPGain',
    'PosIGain',
    'PosDGain',
    'VelScalerGain',
    'VelPGain',
    'VelIGain',
    'VelDGain',
    'TorqueScalerGain',
    'TorquePGain',
    'TorqueIGain',
    'TorqueDGain',
    'SetPosition',
    'SetTorque',
    'SetVelocity',
    'BuzzerEnable',
    'PresentPosition',
    'PresentVelocity',
    'MotorCurrent',
    'InternalRoll',
    'InternalPitch',
    'ExternalRoll',
    'ExternalPitch',
    'AmbientLight',
    'IsButtonPressed',
    'Distance',
    'JoystickX',
    'JoystickY',
    'JoystickButton',
    'QtrR',
    'QtrM',
    'QtrL',
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
