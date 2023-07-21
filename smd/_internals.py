import struct
import enum


class FamilyType():  # Specify Red, Blue and Green types
    pass


class Commands(enum.IntEnum):
    PING = 0x00
    WRITE = 0x01
    WRITE_ACK = 0x80 | 0x01
    READ = 0x02,
    EEPROM_WRITE = 0x03
    SCAN_SENSORS = 0x04
    REBOOT = 0x05
    RESET_ENC = 0x06
    FACTORY_RESET = 0x17
    ERROR_CLEAR = 0x18
    BL_JUMP = 0x30
    SYNC_WRITE = 0x40 | 0x01
    BULK_WRITE = 0x20 | 0x01
    BULK_READ = 0x20 | 0x02
    ACK = 0x80
    __EEPROM_WRITE_ACK = -1


class OperationMode():
    POSITION = 0
    VELOCITY = 1
    TORQUE = 2
    PWM = 3


class Baudrate():
    BAUD115200 = 115200,
    BAUD921600 = 921600,
    BAUD1152000 = 1152000


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
    'TunerEnable',
    'TunerMethod',
    'MotorCPR',
    'MotorRPM',
    'MinimumPositionLimit',
    'MaximumPositionLimit',
    'TorqueLimit',
    'VelocityLimit',
    'PositionFF',
    'VelocityFF',
    'TorqueFF',
    'PositionScalerGain',
    'PositionPGain',
    'PositionIGain',
    'PositionDGain',
    'VelocityScalerGain',
    'VelocityPGain',
    'VelocityIGain',
    'VelocityDGain',
    'TorqueScalerGain',
    'TorquePGain',
    'TorqueIGain',
    'TorqueDGain',
    'SetPosition',
    'SetVelocity',
    'SetTorque',
    'SetDutyCycle',
    'ID11Buzzer',
    'ID12Buzzer',
    'ID13Buzzer',
    'ID14Buzzer',
    'ID15Buzzer',
    'PresentPosition',
    'PresentVelocity',
    'MotorCurrent',
    'AnalogPort'
    'RollAngle',
    'PitchAngle',
    'ID1Button',
    'ID2Button',
    'ID3Button',
    'ID4Button',
    'ID5Button',
    'ID6Light',
    'ID7Light',
    'ID8Light',
    'ID9Light',
    'ID10Light',
    'ID16JoystickX',
    'ID16JoystickY',
    'ID16JoystickButton',
    'ID17JoystickX',
    'ID17JoystickY',
    'ID17JoystickButton',
    'ID18JoystickX',
    'ID18JoystickY',
    'ID18JoystickButton',
    'ID19JoystickX',
    'ID19JoystickY',
    'ID19JoystickButton',
    'ID20JoystickX',
    'ID20JoystickY',
    'ID20JoystickButton',
    'ID21Distance',
    'ID22Distance',
    'ID23Distance',
    'ID24Distance',
    'ID25Distance',
    'ID26QTR',
    'ID27QTR',
    'ID28QTR',
    'ID29QTR',
    'ID30QTR',
    'ID31Servo',
    'ID32Servo',
    'ID33Servo',
    'ID34Servo',
    'ID35Servo',
    'ID36Pot',
    'ID37Pot',
    'ID38Pot',
    'ID39Pot',
    'ID40Pot',
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
