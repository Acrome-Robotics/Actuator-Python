__all__ = ["var",
           "Configuration",
           "Telemetry",
           "Limits",
           "Control",
           "Sensors",
           "CircularBuffer",
           "Index"
           ]


class var():
    def __init__(self, data):
        self.data = data


class Configuration():
    def __init__(self):
        self.devID = var(0)
        self.hardwareVersion = var(0)
        self.softwareVersion = var(0)
        self.baudRate = var(0)
        self.operationMode = var(0)
        self.torqueEnable = var(0)
        self.autotunerEnable = var(0)
        self.autotunerMethod = var(0)
        self.motorCPR = var(0)
        self.motorRPM = var(0)
        self.pwmFreq = var(0)
        self.pwmDuty = var(0)


class Telemetry():
    def __init__(self):
        self.error = var(0)
        self.motorCurrent = var(0)
        self.presentIntRoll = var(0)
        self.presentIntPitch = var(0)
        self.position = var(0)
        self.velocity = var(0)


class Limits():
    def __init__(self):
        self.torqueLimit = var(0)
        self.velocityLimit = var(0)
        self.minPosition = var(0)
        self.maxPosition = var(0)


class Control():
    def __init__(self):
        self.scalerGain = var(0)
        self.proportionalGain = var(0)
        self.integralGain = var(0)
        self.derivativeGain = var(0)
        self.setpoint = var(0)
        self.feedForward = var(0)


class Sensors():
    def __init__(self):
        self.buzzerEnable = var(0)
        self.presentExtRoll = var(0)
        self.presentExtPitch = var(0)
        self.lightIntensity = var(0)
        self.distance = var(0)
        self.buttonPressed = var(0)
        self.joystickX = var(0)
        self.joystickY = var(0)
        self.joystickButton = var(0)
        self.qtrR = var(0)
        self.qtrM = var(0)
        self.qtrL = var(0)


class Index():
    DeviceID = 1
    PackageSize = 2
    Command = 3
    Error = 4
    HardwareVersion = 5
    SoftwareVersion = 6
    Baudrate = 7
    WRITEABLE_INDEX = Baudrate
    OperationMode = 8
    TorqueEnable = 9
    AutotunerEnable = 10
    AutotunerMethod = 11
    MotorCPR = 12
    MotorRPM = 13
    PWMFrequency = 14
    PWMDutyCycle = 15
    MinimumPosition = 16
    MaximumPosition = 17
    TorqueLimit = 18
    VelocityLimit = 19
    PositionFF = 20
    VelocityFF = 21
    TorqueFF = 22
    PosScalerGain = 23
    PosPGain = 24
    PosIGain = 25
    PosDGain = 26
    VelScalerGain = 27
    VelPGain = 28
    VelIGain = 29
    VelDGain = 30
    TorqueScalerGain = 31
    TorquePGain = 32
    TorqueIGain = 33
    TorqueDGain = 34
    SetPosition = 35
    SetTorque = 36
    SetVelocity = 37
    BuzzerEnable = 38
    PresentPosition = 39
    READ_ONLY_INDEX = PresentPosition
    PresentVelocity = 40
    MotorCurrent = 41
    InternalRoll = 42
    InternalPitch = 43
    ExternalRoll = 44
    ExternalPitch = 45
    LightIntensity = 46
    ButtonPressed = 47
    Distance = 48
    JoystickX = 49
    JoystickY = 50
    JoystickButton = 51
    QtrR = 52
    QtrM = 53
    QtrL = 54
    LAST_INDEX = QtrL


class OperationModes():
    POSITION_CONTROL = 0
    VELOCITY_CONTROL = 1
    TORQUE_CONTROL = 2
    PWM_CONTROL = 3
    ANALOG_INPUT = 1 << 7


class AutotuneMethods():
    COHEN_COON = 0,
    ZIEGLER_NICHOLS = 1,


class Errors:
    NoError = 0
    InputVoltageError = 1
    OverheatError = 1 << 1
    OverloadError = 1 << 2
    EncoderError = 1 << 3
    CommunicationError = 1 << 4
    FlashError = 1 << 5


class CircularBuffer():
    def __init__(self, size):
        self.buffer = [0] * size
        self.writePos = 0
        self.readPos = 0
        self.size = size

    def write(self, data):
        if not self._buffer_length() == self.size - 1:
            self.buffer[self.writePos] = int(data)
            self.writePos = ((self.writePos + 1) & (self.size - 1))
            return True
        else:
            return False

    def read(self):
        if self._buffer_length() > 0:
            readPos = self.readPos
            self.readPos = ((self.readPos + 1) & (self.size - 1))
            return self.buffer[readPos]
        else:
            return None

    def peek(self, index_offset=0):
        return self.buffer[(self.readPos + index_offset) & (self.size - 1)]

    def jump(self, offset):
        if offset <= self.availableData():
            self.readPos = (self.readPos + offset) & (self.size - 1)
            return True
        else:
            return False

    def _buffer_length(self):
        return (self.writePos - self.readPos) & (self.size - 1)

    def availableData(self):
        return self._buffer_length()
