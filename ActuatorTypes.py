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
