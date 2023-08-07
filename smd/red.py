from smd._internals import _Data, Index, Commands
import struct
from crccheck.crc import Crc32Mpeg2 as CRC32
import serial
import time
from packaging.version import parse as parse_version


class Red():
    _HEADER = 0x55
    _PRODUCT_TYPE = 0xBA
    _PACKAGE_ESSENTIAL_SIZE = 6
    _STATUS_KEY_LIST = ['EEPROM', 'Software Version', 'Hardware Version']

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
            _Data(Index.TunerEnable, 'B'),
            _Data(Index.TunerMethod, 'B'),
            _Data(Index.MotorShaftCPR, 'f'),
            _Data(Index.MotorShaftRPM, 'f'),
            _Data(Index.UserIndicator, 'B'),
            _Data(Index.MinimumPositionLimit, 'i'),
            _Data(Index.MaximumPositionLimit, 'i'),
            _Data(Index.TorqueLimit, 'H'),
            _Data(Index.VelocityLimit, 'H'),
            _Data(Index.PositionFF, 'f'),
            _Data(Index.VelocityFF, 'f'),
            _Data(Index.TorqueFF, 'f'),
            _Data(Index.PositionDeadband, 'f'),
            _Data(Index.VelocityDeadband, 'f'),
            _Data(Index.TorqueDeadband, 'f'),
            _Data(Index.PositionOutputLimit, 'f'),
            _Data(Index.VelocityOutputLimit, 'f'),
            _Data(Index.TorqueOutputLimit, 'f'),
            _Data(Index.PositionScalerGain, 'f'),
            _Data(Index.PositionPGain, 'f'),
            _Data(Index.PositionIGain, 'f'),
            _Data(Index.PositionDGain, 'f'),
            _Data(Index.VelocityScalerGain, 'f'),
            _Data(Index.VelocityPGain, 'f'),
            _Data(Index.VelocityIGain, 'f'),
            _Data(Index.VelocityDGain, 'f'),
            _Data(Index.TorqueScalerGain, 'f'),
            _Data(Index.TorquePGain, 'f'),
            _Data(Index.TorqueIGain, 'f'),
            _Data(Index.TorqueDGain, 'f'),
            _Data(Index.SetPosition, 'f'),
            _Data(Index.SetVelocity, 'f'),
            _Data(Index.SetTorque, 'f'),
            _Data(Index.SetDutyCycle, 'f'),
            _Data(Index.ID11Buzzer, 'B'),
            _Data(Index.ID12Buzzer, 'B'),
            _Data(Index.ID13Buzzer, 'B'),
            _Data(Index.ID14Buzzer, 'B'),
            _Data(Index.ID15Buzzer, 'B'),
            _Data(Index.PresentPosition, 'f'),
            _Data(Index.PresentVelocity, 'f'),
            _Data(Index.MotorCurrent, 'f'),
            _Data(Index.AnalogPort, 'H'),
            _Data(Index.RollAngle, 'f'),
            _Data(Index.PitchAngle, 'f'),
            _Data(Index.ID1Button, 'B'),
            _Data(Index.ID2Button, 'B'),
            _Data(Index.ID3Button, 'B'),
            _Data(Index.ID4Button, 'B'),
            _Data(Index.ID5Button, 'B'),
            _Data(Index.ID6Light, 'H'),
            _Data(Index.ID7Light, 'H'),
            _Data(Index.ID8Light, 'H'),
            _Data(Index.ID9Light, 'H'),
            _Data(Index.ID10Light, 'H'),
            _Data(Index.ID16JoystickX, 'f'),
            _Data(Index.ID16JoystickY, 'f'),
            _Data(Index.ID16JoystickButton, 'B'),
            _Data(Index.ID17JoystickX, 'f'),
            _Data(Index.ID17JoystickY, 'f'),
            _Data(Index.ID17JoystickButton, 'B'),
            _Data(Index.ID18JoystickX, 'f'),
            _Data(Index.ID18JoystickY, 'f'),
            _Data(Index.ID18JoystickButton, 'B'),
            _Data(Index.ID19JoystickX, 'f'),
            _Data(Index.ID19JoystickY, 'f'),
            _Data(Index.ID19JoystickButton, 'B'),
            _Data(Index.ID20JoystickX, 'f'),
            _Data(Index.ID20JoystickY, 'f'),
            _Data(Index.ID20JoystickButton, 'B'),
            _Data(Index.ID21Distance, 'H'),
            _Data(Index.ID22Distance, 'H'),
            _Data(Index.ID23Distance, 'H'),
            _Data(Index.ID24Distance, 'H'),
            _Data(Index.ID25Distance, 'H'),
            _Data(Index.ID26QTR, 'B'),
            _Data(Index.ID27QTR, 'B'),
            _Data(Index.ID28QTR, 'B'),
            _Data(Index.ID29QTR, 'B'),
            _Data(Index.ID30QTR, 'B'),
            _Data(Index.ID31Servo, 'B'),
            _Data(Index.ID32Servo, 'B'),
            _Data(Index.ID33Servo, 'B'),
            _Data(Index.ID34Servo, 'B'),
            _Data(Index.ID35Servo, 'B'),
            _Data(Index.ID36Pot, 'H'),
            _Data(Index.ID37Pot, 'H'),
            _Data(Index.ID38Pot, 'H'),
            _Data(Index.ID39Pot, 'H'),
            _Data(Index.ID40Pot, 'H'),
            _Data(Index.CRCValue, 'I')
        ]

        if ID > 255 or ID < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        else:
            self.vars[Index.DeviceID].value(ID)

    def get_ack_size(self):
        return self.__ack_size

    def set_variables(self, index_list=[], value_list=[], ack=False):
        self.vars[Index.Command].value(Commands.WRITE_ACK if ack else Commands.WRITE)

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        for index, value in zip(index_list, value_list):
            self.vars[int(index)].value(value)
            fmt_str += 'B' + self.vars[int(index)].type()

        self.__ack_size = struct.calcsize(fmt_str)

        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:6]], *[val for pair in zip(index_list, [self.vars[int(index)].value() for index in index_list]) for val in pair]]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def get_variables(self, index_list=[]):
        self.vars[Index.Command].value(Commands.READ)

        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        fmt_str += 'B' * len(index_list)

        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type()) \
            + struct.calcsize('<' + ''.join(self.vars[idx].type() for idx in index_list))

        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:6]], *[int(idx) for idx in index_list]]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()

        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def reboot(self):
        self.vars[Index.Command].value(Commands.REBOOT)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = 0

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def hard_reset(self):
        self.vars[Index.Command].value(Commands.HARD_RESET)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = 0

        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def EEPROM_write(self, ack=False):
        self.vars[Index.Command].value(Commands.__EEPROM_WRITE_ACK if ack else Commands.EEPROM_WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def ping(self):
        self.vars[Index.Command].value(Commands.PING)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def reset_enc(self):
        self.vars[Index.Command].value(Commands.RESET_ENC)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def scan_sensors(self):
        self.vars[Index.Command].value(Commands.SCAN_SENSORS)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = struct.calcsize(fmt_str + self.vars[Index.CRCValue].type())
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def enter_bootloader(self):
        self.vars[Index.Command].value(Commands.BL_JUMP)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in self.vars[:6]]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[Index.CRCValue].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        self.__ack_size = 0
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())

    def update_id(self, id):
        self.vars[Index.Command].value(Commands.WRITE)
        fmt_str = '<' + ''.join([var.type() for var in self.vars[:6]])
        fmt_str += 'B' + self.vars[int(Index.DeviceID)].type()
        struct_out = list(struct.pack(fmt_str, *[*[var.value() for var in self.vars[:6]], int(Index.DeviceID), id]))
        struct_out[int(Index.PackageSize)] = len(struct_out) + self.vars[int(Index.CRCValue)].size()
        self.vars[Index.CRCValue].value(CRC32.calc(struct_out))
        return bytes(struct_out) + struct.pack('<' + self.vars[Index.CRCValue].type(), self.vars[Index.CRCValue].value())


class Master():
    _BROADCAST_ID = 0xFF

    def __init__(self, portname, baudrate=115200) -> None:
        self.__driver_list = [Red(255)] * 256
        if baudrate > 12500000 or baudrate < 3053:
            raise ValueError('Baudrate must be between 3.053 KBits/s and 12.5 MBits/s.')
        else:
            self.__baudrate = baudrate
            self.__post_sleep = 10 / self.__baudrate
            self.__ph = serial.Serial(port=portname, baudrate=self.__baudrate, timeout=0.1)

    def __del__(self):
        try:
            self.__ph.reset_input_buffer()
            self.__ph.reset_output_buffer()
            self.__ph.close()
        except Exception as e:
            raise e

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

    def attach(self, driver: Red):
        self.__driver_list[driver.vars[Index.DeviceID].value()] = driver

    def detach(self, id):
        self.__driver_list[id] = Red(255)

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
        time.sleep(self.__post_sleep)
        if self.__read_ack(id):
            return [self.__driver_list[id].vars[index].value() for index in index_list]
        else:
            return [None]

    def parse(self, data):
        id = data[Index.DeviceID]
        data = data[6:-4]
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
                if ret[int(Index.PackageSize)] > 10:
                    self.parse(ret)
                    return True
                else:
                    return True  # Ping package
            else:
                return False
        else:
            return False

    def sync_write(self, index: Index, id_val_pairs=[]):
        dev = Red(self.__class__._BROADCAST_ID)
        dev.vars[Index.Command].value(Commands.SYNC_WRITE)

        fmt_str = '<' + ''.join([var.type() for var in dev.vars[:6]])
        struct_out = list(struct.pack(fmt_str, *[var.value() for var in dev.vars[:6]]))

        fmt_str += 'B'
        struct_out += list(struct.pack('<B', int(index)))

        for pair in id_val_pairs:
            fmt_str += 'B'
            struct_out += list(struct.pack('<B', pair[0]))
            struct_out += list(struct.pack('<' + dev.vars[index].type(), pair[1]))

        struct_out[int(Index.PackageSize)] = len(struct_out) + dev.vars[Index.CRCValue].size()
        dev.vars[Index.CRCValue].value(CRC32.calc(struct_out))

        self.__write_bus(bytes(struct_out) + struct.pack('<' + dev.vars[Index.CRCValue].type(), dev.vars[Index.CRCValue].value()))
        time.sleep(self.__post_sleep)

    def __sync_read(self, id):
        raise NotImplementedError()

    def __bulk_write(self, id):
        raise NotImplementedError()

    def __bulk_read(self, id):
        raise NotImplementedError()

    def scan(self) -> list:
        self.__ph.timeout(0.015)
        connected = []
        for idx in range(255):
            self.attach(Red(idx))
            if self.ping(idx):
                connected.append(idx)
            else:
                self.detach(idx)
        self.__ph.timeout(0.1)
        return connected

    def update_board_baudrate(self, id, br):
        if br > 12500000 or br < 3053:
            raise ValueError('Baudrate must be between 3.053 KBits/s and 12.5 MBits/s.')

        self.set_variables(id, [[Index.Baudrate, br]])
        time.sleep(self.__post_sleep)
        self.eeprom_write(id)
        time.sleep(self.__post_sleep)
        self.reboot(id)

    def update_master_baudrate(self, br):
        self.__ph.reset_input_buffer()
        self.__ph.reset_output_buffer()
        try:
            settings = self.__ph.get_settings()
            self.__ph.close()
            settings['baudrate'] = br
            self.__ph.apply_settings(settings)
            self.__ph.open()

            self.__post_sleep = 10 / br

        except Exception as e:
            raise e

    def reboot(self, id):
        self.__write_bus(self.__driver_list[id].reboot())
        time.sleep(self.__post_sleep)

    def hard_reset(self, id):
        self.__write_bus(self.__driver_list[id].hard_reset())
        time.sleep(self.__post_sleep)

    def eeprom_write(self, id, ack=False):
        self.__write_bus(self.__driver_list[id].EEPROM_write(ack=ack))
        time.sleep(self.__post_sleep)

        if ack:
            if self.__read_ack(id):
                return True
            else:
                return False

    def ping(self, id) -> bool:
        self.__write_bus(self.__driver_list[id].ping())
        time.sleep(self.__post_sleep)

        if self.__read_ack(id):
            return True
        else:
            return False

    def reset_enc(self, id):
        self.__write_bus(self.__driver_list[id].reset_enc())
        time.sleep(self.__post_sleep)

    def scan_sensors(self, id) -> list:
        connected = []
        self.__write_bus(self.__driver_list[id].scan_sensors())
        time.sleep(self.__post_sleep)

        return connected

    def enter_bootloader(self, id):
        self.__write_bus(self.__driver_list[id].enter_bootloader())
        time.sleep(self.__post_sleep)

    def get_board_info(self, id):
        st = dict()
        data = self.get_variables(id, [Index.Status, Index.HardwareVersion, Index.SoftwareVersion])
        if data is not None:
            st['HardwareVersion'] = data[1]
            st['SoftwareVersion'] = data[2]
            return st
        else:
            return None

    def update_board_id(self, id, id_new):
        if id_new > 255 or id_new < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        self.__write_bus(self.__driver_list[id].update_id(id_new))
        time.sleep(self.__post_sleep)

    def enable_torque(self, id, en: bool):
        self.set_variables(id, [[Index.TorqueEnable, en]])
        time.sleep(self.__post_sleep)

    def set_operation_mode(self, id, mode):
        self.set_variables(id, [[Index.OperationMode, mode]])
        time.sleep(self.__post_sleep)

    def get_operation_mode(self, id):
        return self.get_variables(id, [Index.OperationMode])

    def set_shaft_cpr(self, id, cpr):
        self.set_variables(id, [[Index.MotorShaftCPR, cpr]])
        time.sleep(self.__post_sleep)

    def set_shaft_rpm(self, id, rpm):
        self.set_variables(id, [[Index.MotorShaftRPM, rpm]])
        time.sleep(self.__post_sleep)

    def set_user_indicator(self, id):
        self.set_variables(id, [[Index.UserIndicator, 1]])
        time.sleep(self.__post_sleep)   

    def set_position_limits(self, id, plmin, plmax):
        self.set_variables(id, [[Index.MinimumPositionLimit, plmin], [Index.MaximumPositionLimit, plmax]])
        time.sleep(self.__post_sleep)

    def get_position_limits(self, id):
        return self.get_variables(id, [Index.MinimumPositionLimit, Index.MaximumPositionLimit])

    def set_torque_limit(self, id, tl):
        self.set_variables(id, [[Index.TorqueLimit, tl]])
        time.sleep(self.__post_sleep)

    def get_torque_limit(self, id):
        return self.get_variables(id, [Index.TorqueLimit])

    def set_velocity_limit(self, id, vl):
        self.set_variables(id, [[Index.VelocityLimit, vl]])
        time.sleep(self.__post_sleep)

    def get_velocity_limit(self, id):
        return self.get_variables(id, [Index.VelocityLimit])

    def set_position(self, id, sp):
        self.set_variables(id, [[Index.SetPosition, sp]])
        time.sleep(self.__post_sleep)

    def get_position(self, id):
        return self.get_variables(id, [Index.PresentPosition])

    def set_velocity(self, id, sp):
        self.set_variables(id, [[Index.SetVelocity, sp]])
        time.sleep(self.__post_sleep)

    def get_velocity(self, id):
        return self.get_variables(id, [Index.PresentVelocity])

    def set_torque(self, id, sp):
        self.set_variables(id, [[Index.SetTorque, sp]])
        time.sleep(self.__post_sleep)

    def get_torque(self, id):
        return self.get_variables(id, [Index.MotorCurrent])

    def set_duty_cycle(self, id, pct):
        self.set_variables(id, [[Index.SetDutyCycle, pct]])
        time.sleep(self.__post_sleep)

    def get_analog_port(self, id):
        return self.get_variables(id, [Index.AnalogPort])

    def set_control_parameters_position(self, id, p=None, i=None, d=None, db=None, ff=None, out_lim=None):
        index_list = [Index.PositionPGain, Index.PositionIGain, Index.PositionDGain, Index.PositionDeadband, Index.PositionFF, Index.PositionOutputLimit]
        val_list = [p, i, d, db, ff, out_lim]

        self.set_variables(id, [list(pair) for pair in zip(index_list, val_list) if pair[1] is not None])
        time.sleep(self.__post_sleep)

    def get_control_parameters_position(self, id):
        return self.get_variables(id, [Index.PositionPGain, Index.PositionIGain, Index.PositionDGain, Index.PositionDeadband, Index.PositionFF, Index.PositionOutputLimit])

    def set_control_parameters_velocity(self, id, p=None, i=None, d=None, db=None, ff=None, out_lim=None):
        index_list = [Index.VelocityPGain, Index.VelocityIGain, Index.VelocityDGain, Index.VelocityDeadband, Index.VelocityFF, Index.VelocityOutputLimit]
        val_list = [p, i, d, db, ff, out_lim]

        self.set_variables(id, [list(pair) for pair in zip(index_list, val_list) if pair[1] is not None])
        time.sleep(self.__post_sleep)

    def get_control_parameters_velocity(self, id):
        return self.get_variables(id, [Index.VelocityPGain, Index.VelocityIGain, Index.VelocityDGain, Index.VelocityDeadband, Index.VelocityFF, Index.VelocityOutputLimit])

    def set_control_parameters_torque(self, id, p=None, i=None, d=None, db=None, ff=None, out_lim=None):
        index_list = [Index.TorquePGain, Index.TorqueIGain, Index.TorqueDGain, Index.TorqueDeadband, Index.TorqueFF, Index.TorqueOutputLimit]
        val_list = [p, i, d, db, ff, out_lim]

        self.set_variables(id, [list(pair) for pair in zip(index_list, val_list) if pair[1] is not None])
        time.sleep(self.__post_sleep)

    def get_control_parameters_torque(self, id):
        return self.get_variables(id, [Index.TorquePGain, Index.TorqueIGain, Index.TorqueDGain, Index.TorqueDeadband, Index.TorqueFF, Index.TorqueOutputLimit])
