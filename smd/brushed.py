from smd._internals import _Data, Index, Commands
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import serial
import time


class Brushed():
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
            _Data(Index.HardwareVersion, 'I'),
            _Data(Index.SoftwareVersion, 'I'),
            _Data(Index.Baudrate, 'I'),
            _Data(Index.OperationMode, 'B'),
            _Data(Index.TorqueEnable, 'B'),
            _Data(Index.AutotunerEnable, 'B'),
            _Data(Index.AutotuneMethod, 'B'),
            _Data(Index.MotorCPR, 'f'),
            _Data(Index.MotorRPM, 'f'),
            _Data(Index.PWMFrequency, 'I'),
            _Data(Index.SetDutyCycle, 'f'),
            _Data(Index.MinimumPosition, 'i'),
            _Data(Index.MaximumPosition, 'i'),
            _Data(Index.TorqueLimit, 'H'),
            _Data(Index.VelocityLimit, 'H'),
            _Data(Index.PositionFF, 'f'),
            _Data(Index.VelocityFF, 'f'),
            _Data(Index.TorqueFF, 'f'),
            _Data(Index.PosScalerGain, 'f'),
            _Data(Index.PosPGain, 'f'),
            _Data(Index.PosIGain, 'f'),
            _Data(Index.PosDGain, 'f'),
            _Data(Index.VelScalerGain, 'f'),
            _Data(Index.VelPGain, 'f'),
            _Data(Index.VelIGain, 'f'),
            _Data(Index.VelDGain, 'f'),
            _Data(Index.TorqueScalerGain, 'f'),
            _Data(Index.TorquePGain, 'f'),
            _Data(Index.TorqueIGain, 'f'),
            _Data(Index.TorqueDGain, 'f'),
            _Data(Index.SetPosition, 'f'),
            _Data(Index.SetTorque, 'f'),
            _Data(Index.SetVelocity, 'f'),
            _Data(Index.BuzzerEnable, 'B'),
            _Data(Index.PresentPosition, 'f'),
            _Data(Index.PresentVelocity, 'f'),
            _Data(Index.MotorCurrent, 'f'),
            _Data(Index.InternalRoll, 'f'),
            _Data(Index.InternalPitch, 'f'),
            _Data(Index.ExternalRoll, 'f'),
            _Data(Index.ExternalPitch, 'f'),
            _Data(Index.AmbientLight, 'H'),
            _Data(Index.IsButtonPressed, 'B'),
            _Data(Index.Distance, 'H'),
            _Data(Index.JoystickX, 'H'),
            _Data(Index.JoystickY, 'H'),
            _Data(Index.JoystickButton, 'B'),
            _Data(Index.QtrR, 'B'),
            _Data(Index.QtrM, 'B'),
            _Data(Index.QtrL, 'B'),
            _Data(Index.CRCValue, 'I'),
        ]

        if ID > 255 or ID < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        else:
            self.vars[Index.DeviceID].value(ID)

    def get_ack_size(self):
        return self.__ack_size

    def set_variables(self, index_list=[], value_list=[], ack=False):
        self.vars[Index.Command].value(Commands.WRITE_ACK if ack else Commands.WRITE)

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

        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type()) \
            + struct.calcsize(''.join(self.vars[idx].type() for idx in index_list))

        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:5]], *[int(idx) for idx in index_list]]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def reboot(self):
        self.vars[Index.Command].value(Commands.REBOOT)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = 0
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def EEPROM_write(self, ack=False):
        self.vars[Index.Command].value(Commands.__EEPROM_WRITE_ACK if ack else Commands.EEPROM_WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def ping(self):
        self.vars[Index.Command].value(Commands.PING)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:5]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def update_id(self, id):
        self.vars[Index.Command].value(Commands.WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:5]])
        fmt_str += 'B' + self.vars[int(Index.DeviceID)].type()
        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:5]], int(Index.DeviceID), id]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())


class Master():
    _BROADCAST_ID = 0xFF

    def __init__(self, portname, baudrate=115200) -> None:
        self.__driver_list = [Brushed(255)] * 256
        if baudrate > 6250000 or baudrate < 1537:
            raise ValueError('Baudrate must be in range of 1537 to 6.25M')
        else:
            self.__baudrate = baudrate
            self.__post_sleep = 10 / self.__baudrate
            self.__ph = serial.Serial(port=portname, baudrate=self.__baudrate, timeout=0.1)

    def __del__(self):
        try:
            self.__ph.reset_input_buffer()
            self.__ph.reset_output_buffer()
            self.__ph.close()
        except:
            pass

    def __write_bus(self, data):
        self.__ph.write(data)

    def __read_bus(self, size) -> bytes:
        self.__ph.reset_input_buffer()
        return self.__ph.read(size=size)

    def update_id(self, id, id_new):
        if id_new > 255 or id_new < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        self.__write_bus(self.__driver_list[id].change_id(id_new))

    def update_baudrate(self, baud: int):
        self.__ph.reset_input_buffer()
        self.__ph.reset_output_buffer()

        try:
            self.__ph.baudrate(baud)
        except:
            pass

    def attach(self, driver: Brushed):
        self.__driver_list[driver.vars[Index.DeviceID].value()] = driver

    def detach(self, id):
        self.__driver_list[id] = Brushed(255)

    def set_variables(self, id, idx_val_pairs=[], ack=False):
        index_list = [pair[0] for pair in idx_val_pairs]
        value_list = [pair[1] for pair in idx_val_pairs]
        self.__write_bus(self.__driver_list[id].set_variables(index_list, value_list, ack))
        if ack:
            self.__read_ack(id)
            return [self.__driver_list[id].vars[index].value() for index in index_list]
        time.sleep(self.__post_sleep)
        return [None]

    def get_variables(self, id, index_list) -> list:
        self.__write_bus(self.__driver_list[id].get_variables(index_list))
        if self.__read_ack(id):
            return [self.__driver_list[id].vars[index].value() for index in index_list]
        else:
            return [None]

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
                    return True  # Ping package
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
            self.attach(Brushed(idx))
            if self.ping(idx):
                connected.append(idx)
            else:
                self.detach(idx)
        return connected
