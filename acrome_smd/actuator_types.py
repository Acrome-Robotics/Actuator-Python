from enum import IntEnum


class var():
    def __init__(self, data):
        self.data = data


class Configuration():
    def __init__(self):
        self.devID = var(0)
        self.operationMode = var(0)
        self.torqueEnable = var(0)
        self.autotunerEnable = var(0)
        self.modelNum = var(0)
        self.firmwareVersion = var(0)
        self.baudRate = var(0)


class Telemetry():
    def __init__(self):
        self.error = var(0)
        self.errorCount = var(0)
        self.voltage = var(0)
        self.temperature = var(0)
        self.current = var(0)
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
        self.presentRoll = var(0)
        self.presentPitch = var(0)
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
    deviceId = 1
    error = 4
    baudrate = 5
    WRITEABLE_INDEX = baudrate
    operationMode = 6
    tempLimit = 7
    torqueEnable = 8
    autotunerEnable = 9
    RGB = 10
    minVoltage = 11
    maxVoltage = 12
    torqueLimit = 13
    velocityLimit = 14
    autotunerMethod = 15
    posFeedForward = 16
    velFeedForward = 17
    torqueFeedForward = 18
    posScalerGain = 19
    posPGain = 20
    posIGain = 21
    posDGain = 22
    velScalerGain = 23
    velPGain = 24
    velIGain = 25
    velDGain = 26
    torqueScalerGain = 27
    torquePGain = 28
    torqueIGain = 29
    torqueDGain = 30
    homeOffset = 31
    minPosition = 32
    maxPosition = 33
    posSetpoint = 34
    torqueSetpoint = 35
    velSetpoint = 36
    buzzerEnable = 37
    presentPos = 38
    READ_ONLY_INDEX = presentPos
    presentVel = 39
    presentVoltage = 40
    presentTemp = 41
    presentCurrent = 42
    presentRoll = 43
    presentPitch = 44
    lightIntensity = 45
    buttonPressed = 46
    usDistance = 47
    joystickX = 48
    joystickY = 49
    joystickButton = 50
    qtrR = 51
    qtrM = 52
    qtrL = 53
    ModelNum = 54
    FirmwareVersion = 55
    errorCount = 56
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
