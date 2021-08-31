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

class ExternalPort():
	def __init__(self):
		self.portMode = var(0)
		self.portData = var(0)

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

class Parameters():
	deviceId = 1
	error = 4
	baudrate = 5
	operationMode = 6
	tempLimit = 7
	PIOMode = 8
	torqueEnable = 9
	RGB = 10
	minVoltage = 11
	maxVoltage = 12
	torqueLimit = 13
	velocityLimit = 14
	posFeedForward = 15
	velFeedForward = 16
	torqueFeedForward = 17
	posPGain = 18
	posIGain = 19
	posDGain = 20
	velPGain = 21
	velIGain = 22
	velDGain = 23
	torquePGain = 24
	torqueIGain = 25
	torqueDGain = 26
	homeOffset = 27
	minPosition = 28
	maxPosition = 29
	posSetpoint = 30
	torqueSetpoint = 31
	velSetpoint = 32
	presentPos = 33
	presentVel = 34
	presentVoltage = 35
	presentTemp = 36
	presentCurrent = 37
	ModelNum = 38
	FirmwareVersion = 39
	errorCount = 40

class CircularBuffer():
	def __init__(self, size):
		self.buffer = [0] * size
		self.writePos = 0
		self.readPos = 0
		self.size = size

	def write(self, data):
		if not self._buffer_length() == self.size - 1:
			self.buffer[self.writePos] = int(data)
			self.writePos += 1
			if self.writePos > self.size-1:
				self.writePos = 0
			return True
		else:
			return False

	def read(self):
		if self._buffer_length() != 0:
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