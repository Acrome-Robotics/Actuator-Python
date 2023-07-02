from smd._internals import _Data, Index


class SMDRed():
    def __init__(self, ID: int) -> None:
        _BROADCAST_ID = 0xFF
        _PRODUCT_TYPE = None
        _PACKAGE_ESSENTIAL_SIZE = 5

        self.vars = [
            _Data(Index.Header, 'B', False, 0x55),
            _Data(Index.DeviceID, 'B'),
            _Data(Index.PackageSize, 'B'),
            _Data(Index.Command, 'B'),
            _Data(Index.Error, 'B'),
            _Data(Index.Baudrate, 'I'),
            _Data(Index.OperationMode, 'B'),
            _Data(Index.CRCValue, 'I'),
        ]

        if ID > 255 or ID < 0:
            raise ValueError("Device ID can not be higher than 254 or lower than 0!")
        else:
            self.vars[Index.DeviceID].value(ID)

    def set_variables(self):
        pass

    def get_variables(self):
        pass

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
