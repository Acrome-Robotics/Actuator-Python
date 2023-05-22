from enum import IntEnum

__all__ = ["var",
           "Configuration",
           "Telemetry",
           "Limits",
           "Control",
           "Autotuner",
           "Sensors",
           "CircularBuffer",
           "Parameters"
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
        self.motor_cpr = var(0)
        self.motor_rpm = var(0)
        self.pwm_freq = var(0)
        self.pwm_duty = var(0)


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
    deviceId = 1
    __RESERVED1 = 2
    __RESERVED2 = 3
    error = 4
    hardwareVersion = 5
    softwareVersion = 6
    baudrate = 7
    WRITEABLE_INDEX = baudrate
    operationMode = 8
    torqueEnable = 9
    autotunerEnable = 10
    motorCPR = 11
    motorRPM = 12
    pwmFreq = 13
    torqueLimit = 14
    velocityLimit = 15
    autotunerMethod = 16
    posFeedForward = 17
    velFeedForward = 18
    torqueFeedForward = 19
    posScalerGain = 20
    posPGain = 21
    posIGain = 22
    posDGain = 23
    velScalerGain = 24
    velPGain = 25
    velIGain = 26
    velDGain = 27
    torqueScalerGain = 28
    torquePGain = 29
    torqueIGain = 30
    torqueDGain = 31
    minPosition = 32
    maxPosition = 33
    posSetpoint = 34
    torqueSetpoint = 35
    velSetpoint = 36
    pwmDutySetpoint = 37
    buzzerEnable = 38
    presentPos = 39
    READ_ONLY_INDEX = presentPos
    presentVel = 40
    presentMotorCurrent = 41
    presentIntRoll = 42
    presentIntPitch = 43
    presentExtRoll = 44
    presentExtPitch = 45
    lightIntensity = 46
    buttonPressed = 47
    usDistance = 48
    joystickX = 49
    joystickY = 50
    joystickButton = 51
    qtrR = 52
    qtrM = 53
    qtrL = 54
    LAST_INDEX = qtrL


class OperationModes(IntEnum):
    POSITION_CONTROL = 0
    VELOCITY_CONTROL = 1
    TORQUE_CONTROL = 2
    PWM_CONTROL = 3
    ANALOG_INPUT = 1 << 7


class AutotuneMethods(IntEnum):
    NO_METHOD_SELECTED = 0
    __RESERVED = 1,
    ZIEGLER_NICHOLS = 2,
    COHEN_COON = 3,


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
