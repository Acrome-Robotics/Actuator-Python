from enum import IntEnum, auto


class var():
    def __init__(self, data):
        self.data = data


class Configuration():
    def __init__(self):
        self.devID = var(0)
        self.operationMode = var(0)
        self.torqueEnable = var(0)
        self.autotunerEnable = var(0)
        self.motPwmFreq = var(0)
        self.modelNum = var(0)
        self.firmwareVersion = var(0)
        self.baudRate = var(0)


class Telemetry():
    def __init__(self):
        self.error = var(0)
        self.errorCount = var(0)
        self.voltage = var(0)
        self.coreTemperature = var(0)
        self.motorTemperature = var(0)
        self.motorCurrent = var(0)
        self.presentIntRoll = var(0)
        self.presentIntPitch = var(0)
        self.position = var(0)
        self.velocity = var(0)


class Limits():
    def __init__(self):
        self.temperatureLimit = var(0)
        self.minVoltage = var(0)
        self.maxVoltage = var(0)
        self.torqueLimit = var(0)
        self.velocityLimit = var(0)
        self.minPosition = var(0)
        self.maxPosition = var(0)
        self.homeOffset = var(0)


class Indicators():
    def __init__(self):
        self.RGB = var(0)
        self.LEDs = var(0)


class Control():
    def __init__(self):
        self.scalerGain = var(0)
        self.proportionalGain = var(0)
        self.integralGain = var(0)
        self.derivativeGain = var(0)
        self.setpoint = var(0)
        self.feedForward = var(0)


class Autotuner():
    def __init__(self):
        self.method = var(0)


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


class Parameters(IntEnum):
    deviceId = auto()
    __RESERVED1 = auto()
    __RESERVED2 = auto()
    error = auto()
    baudrate = auto()
    WRITEABLE_INDEX = baudrate
    operationMode = auto()
    motorPwmFreq = auto()
    tempLimit = auto()
    torqueEnable = auto()
    autotunerEnable = auto()
    minVoltage = auto()
    maxVoltage = auto()
    torqueLimit = auto()
    velocityLimit = auto()
    autotunerMethod = auto()
    posFeedForward = auto()
    velFeedForward = auto()
    torqueFeedForward = auto()
    posScalerGain = auto()
    posPGain = auto()
    posIGain = auto()
    posDGain = auto()
    velScalerGain = auto()
    velPGain = auto()
    velIGain = auto()
    velDGain = auto()
    torqueScalerGain = auto()
    torquePGain = auto()
    torqueIGain = auto()
    torqueDGain = auto()
    homeOffset = auto()
    minPosition = auto()
    maxPosition = auto()
    posSetpoint = auto()
    torqueSetpoint = auto()
    velSetpoint = auto()
    buzzerEnable = auto()
    presentPos = auto()
    READ_ONLY_INDEX = presentPos
    presentVel = auto()
    presentVoltage = auto()
    presentCoreTemp = auto()
    presentMotorTemp = auto()
    presentMotorCurrent = auto()
    presentIntRoll = auto()
    presentIntPitch = auto()
    presentExtRoll = auto()
    presentExtPitch = auto()
    lightIntensity = auto()
    buttonPressed = auto()
    usDistance = auto()
    joystickX = auto()
    joystickY = auto()
    joystickButton = auto()
    qtrR = auto()
    qtrM = auto()
    qtrL = auto()
    ModelNum = auto()
    FirmwareVersion = auto()
    errorCount = auto()
    LAST_INDEX = errorCount


class OperationModes:
    PositionControl = 0
    VelocityControl = 1
    TorqueControl = 2
    AnalogInput = 1 << 7


class AutotuneMethods:
    NoneMethod = 0
    BasicMeasurement = 1,
    ZieglerNichols = 2,
    CohenCoon = 3,


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