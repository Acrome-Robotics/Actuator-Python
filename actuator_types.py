from enum import IntEnum


class var():
	def __init__(self, data):
		self.data = data


class Configuration():
	def __init__(self):
		self.devID = var(0)
		self.operationMode = var(0)
		self.torqueEnable = var(0)
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
		self.proportionalGain = var(0)
		self.integralGain = var(0)
		self.derivativeGain = var(0)
		self.setpoint = var(0)
		self.feedForward = var(0)

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
		self.qtr = var(0)
		

class Parameters(IntEnum):
	deviceId = 1
	error = 4
	baudrate = 5
	WRITEABLE_INDEX = baudrate
	operationMode = 6
	tempLimit = 7
	torqueEnable = 8
	RGB = 9
	minVoltage = 10
	maxVoltage = 11
	torqueLimit = 12
	velocityLimit = 13
	posFeedForward = 14
	velFeedForward = 15
	torqueFeedForward = 16
	posPGain = 17
	posIGain = 18
	posDGain = 19
	velPGain = 20
	velIGain = 21
	velDGain = 22
	torquePGain = 23
	torqueIGain = 24
	torqueDGain = 25
	homeOffset = 26
	minPosition = 27
	maxPosition = 28
	posSetpoint = 29
	torqueSetpoint = 30
	velSetpoint = 31
	buzzerEnable = 32,
	presentPos = 33
	READ_ONLY_INDEX = presentPos
	presentVel = 34
	presentVoltage = 35
	presentTemp = 36
	presentCurrent = 37
	presentRoll = 38
	presentPitch = 39
	lightIntensity = 40
	buttonPressed = 41
	usDistance = 42
	joystickX = 43
	joystickY = 44
	qtr = 45
	ModelNum = 46
	FirmwareVersion = 47
	errorCount = 48
	LAST_INDEX = errorCount


class OperationModes:
	PositionControl = 0
	VelocityControl = 1
	TorqueControl = 2
	AnalogInput = 1 << 7


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
			self.readPos = ((self.readPos + 1) & ( self.size - 1 ))
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
