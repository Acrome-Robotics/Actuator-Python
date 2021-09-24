import time
from crccheck.crc import Crc32Mpeg2 as CRC32
from actuator_types import *
from ctypes import *
import struct
import serial

class Actuator():
	BATCH_ID = 0xFF
	HEADER = 0x55
	_commandLUT = {'Ping':0, 'Write':1, 'Read':2, 'ROMWrite':3, 'Reboot':5, 'FactoryReset':0x17, 'ErrorClear':0x18, 'RQ':1<<7}
	def __init__(self, ID):
		self.header = var(0x55)
		self.packageSize = var(0)
		self.command = var(0)
		self.Configuration = var(Configuration())
		self.Telemetry = var(Telemetry())
		self.Limits = var(Limits())
		self.PositionControl = var(Control())
		self.VelocityControl = var(Control())
		self.TorqueControl = var(Control())
		self.PIOs = var(PIOs())
		self.Indicators = var(Indicators())
		self.CRC = var(0)

		self.Configuration.data.devID.data = ID

		self.Indexes = [
			[(self.header), 1, c_uint8],
			[(self.Configuration.data.devID), 1, c_uint8],
			[(self.packageSize), 1, c_uint8],
			[(self.command), 1, c_uint8],
			[(self.Telemetry.data.error), 1, c_uint8],
			[(self.Configuration.data.baudRate), 4, c_uint32],
			[(self.Configuration.data.operationMode), 1, c_uint8],
			[(self.Limits.data.temperatureLimit),1, c_uint8],
			[(self.PIOs.data.portMode), 5, c_uint8],
			[(self.Configuration.data.torqueEnable), 1, c_uint8],
			[(self.Indicators.data.RGB), 1, c_uint8],
			[(self.Limits.data.minVoltage), 2, c_uint16],
			[(self.Limits.data.maxVoltage), 2, c_uint16],
			[(self.Limits.data.torqueLimit), 2, c_uint16],
			[(self.Limits.data.velocityLimit), 2, c_uint16],
			[(self.PositionControl.data.feedForward), 4, c_float],
			[(self.VelocityControl.data.feedForward), 4, c_float],
			[(self.TorqueControl.data.feedForward), 4, c_float],
			[(self.PositionControl.data.proportionalGain), 4, c_float],
			[(self.PositionControl.data.integralGain), 4, c_float],
			[(self.PositionControl.data.derivativeGain), 4, c_float],
			[(self.VelocityControl.data.proportionalGain), 4, c_float],
			[(self.VelocityControl.data.integralGain), 4, c_float],
			[(self.VelocityControl.data.derivativeGain), 4, c_float],
			[(self.TorqueControl.data.proportionalGain), 4, c_float],
			[(self.TorqueControl.data.integralGain), 4, c_float],
			[(self.TorqueControl.data.derivativeGain), 4, c_float],
			[(self.Limits.data.homeOffset), 4, c_int32],
			[(self.Limits.data.minPosition), 4, c_uint32],
			[(self.Limits.data.maxPosition), 4, c_uint32],
			[(self.PIOs.data.portData), 10, c_uint16],
			[(self.PositionControl.data.setpoint), 4, c_float],
			[(self.TorqueControl.data.setpoint), 4, c_float],
			[(self.VelocityControl.data.setpoint), 4, c_float],
			[(self.Telemetry.data.position), 4, c_float],
			[(self.Telemetry.data.velocity), 4, c_float],
			[(self.Telemetry.data.voltage), 2, c_uint16],
			[(self.Telemetry.data.temperature), 2, c_uint16],
			[(self.Telemetry.data.current), 4, c_float],
			[(self.Configuration.data.modelNum), 4, c_uint32],
			[(self.Configuration.data.firmwareVersion), 4, c_uint32],
			[(self.Telemetry.data.errorCount), 4, c_uint32],
			[(self.CRC), 4, c_uint32]
		]

	def __populate_header(self):
		return self.__class__.HEADER.to_bytes(1,'little') +\
			self.Configuration.data.devID.data.to_bytes(1,'little') +\
			self.packageSize.data.to_bytes(1,'little') +\
			self.command.data.to_bytes(1,'little') +\
			self.Telemetry.data.error.data.to_bytes(1,'little')

	def __calculate_crc(self, data):
		self.CRC = CRC32.calc(data).to_bytes(4, byteorder='little')
		return self.CRC

	def Ping(self):
		self.command.data = self.__class__._commandLUT['Ping']
		self.packageSize.data = 9

		data = self.__populate_header()
		data += self.__calculate_crc(data)
		return data

	def Read(self, params=[], full=False):
		self.command.data = self._commandLUT['Read']

		if full:
			self.packageSize.data = 10
			params = [0xFF]

		else:
			params = [param for param in params if param < len(self.Indexes)] #Safety Check
			self.packageSize.data = 9 + len(params)

		data = self.__populate_header()
		data += bytes(params)
		data += self.__calculate_crc(data)

		return data

	def Write(self, Act, param_list=None):
		params = []

		if param_list is not None:
			if not isinstance(param_list, list):
				param_list = [param_list]
			for param in param_list:
				if self.Indexes[param][0].data != Act.Indexes[param][0].data:
					params.append(param)
		else:
			#Writeable range
			for i in range(5, 34):
				if self.Indexes[i][0].data != Act.Indexes[i][0].data:
					params.append(i)

		updating = bytearray()
		for param in params:
			#Add index to array
			updating.extend(param.to_bytes(1, 'little'))

			#Add actual value to array
			if Act.Indexes[param][2] == c_float:
				updating.extend(struct.pack("<f", Act.Indexes[param][0].data))
			elif Act.Indexes[param][2] in [c_uint8, c_ubyte, c_char]:
				if isinstance(Act.Indexes[param][0].data, list):
					for data in Act.Indexes[param][0].data:
						updating.extend(struct.pack("<B", data.data & 0xFF))
				else:
					updating.extend(struct.pack("<B", Act.Indexes[param][0].data & 0xFF))
			elif Act.Indexes[param][2] == c_uint16:
				if isinstance(Act.Indexes[param][0].data, list):
					for data in list(Act.Indexes[param][0].data):
						updating.extend(struct.pack("<H", data.data & 0xFFFF))
				else:
					updating.extend(struct.pack("<H", Act.Indexes[param][0].data & 0xFFFF))
			elif Act.Indexes[param][2] == c_uint32:
				updating.extend(struct.pack("<I", Act.Indexes[param][0].data & 0xFFFFFFFF))
			elif Act.Indexes[param][2] == c_int32:
				updating.extend(struct.pack("<i", Act.Indexes[param][0].data & 0xFFFFFFFF))

		self.packageSize.data = 9 + len(updating)
		self.command.data = self._commandLUT['Write']

		data = self.__populate_header()
		data += updating
		data += self.__calculate_crc(data)
		return data

	def Reboot(self):
		self.command.data = self.__class__._commandLUT['Reboot']
		self.packageSize.data = 9

		data = self.__populate_header()
		data += self.__calculate_crc(data)
		return data

	def FactoryReset(self):
		self.command.data = self.__class__._commandLUT['FactoryReset']
		self.packageSize.data = 9
		data = self.__populate_header()
		data += self.__calculate_crc(data)
		return data

	def ROMWrite(self):
		self.command.data = self.__class__._commandLUT['ROMWrite']
		self.packageSize.data = 9
		data = self.__populate_header()
		data += self.__calculate_crc(data)
		return data

	#Parse package which is already checked against CRC and package integrity
	def parse(self, package):
		cmds = self.__class__._commandLUT
		self.Telemetry.data.error.data = package[4]
		
		if package[3] == cmds['Read']:
			i = 5
			while i < (len(package) - 4):

				#Check if index is in parameters range
				if package[i] > Parameters.errorCount:
					return
				
				#Floats
				if self.Indexes[package[i]][2] == c_float:
					self.Indexes[package[i]][0].data = struct.unpack('<f', bytes(package[i+1:i+1+self.Indexes[package[i]][1]]))[0]
					i += self.Indexes[package[i]][1]
				#Integers
				else:
					if package[i] == Parameters.PIOData or package[i] == Parameters.PIOMode:
						for var, index in zip(self.Indexes[package[i]][0].data, range(PIOs._pio_count)):
							var.data = int.from_bytes(package[i+1+index:i+1+sizeof(self.Indexes[package[i]][2])+index], 'little')
					else:
						self.Indexes[package[i]][0].data = int.from_bytes(package[i+1:i+1+self.Indexes[package[i]][1]], 'little')

					i += self.Indexes[package[i]][1]

				i+=1

		if package[3] == cmds['Ping']:
			return
		else:
			return

class Master():
	_min_size = 9
	_max_size = 243
	def __init__(self, size, portname, baudrate=115200, master_timeout=0.01) -> None:
		self.cb = CircularBuffer(size)
		self.ActList = []
		self.Actuators = [Actuator(255)] * 255
		self.Timestamps = [0] * 255
		self._serial = ser = serial.Serial(portname, baudrate, timeout=master_timeout)

	def addActuator(self, ID) -> None:
		if ID not in self.ActList:
			self.ActList.append(ID)
			self.Actuators[ID] = Actuator(ID)

	def findPackage(self) -> None:

		#Start parsing only if there is enough data available to contain a valid package
		while self.cb.availableData() >= 9:
			if self.cb.peek(0) == 0x55:
				if self.cb.peek(1) in self.ActList:
					size = self.cb.peek(2)
					#Is package size in valid limits
					if size >= self.__class__._min_size and size <= self.__class__._max_size:

						if size <= self.cb.availableData():

							package = []
							#Check if package is contigous
							if (self.cb.readPos + size) < self.cb.size:
								package = self.cb.buffer[self.cb.readPos:self.cb.readPos + size]

								#return package
							else:
								package = self.cb.buffer[self.cb.readPos:]
								claimed = self.cb.size - self.cb.readPos
								package += self.cb.buffer[:(size - claimed)]
								#return package

							packageCRC = int.from_bytes(package[-4:],'little')
							CalculatedCRC = CRC32.calc(bytearray(package[:-4]))
							if packageCRC == CalculatedCRC:
								if not self.cb.jump(size):
									self.cb.read()
								self.Actuators[package[1]].parse(package)
								self.Timestamps[package[1]] = time.time()
							else:
								#Dummy read
								self.cb.read()

						#Not enough data is present, might be still receiving
						else:
							break
				else:
					#Dummy read
					self.cb.read()
			else:
				#Dummy read
				self.cb.read()

	def removeActuator(self, ID) -> None:
		self.ActList.remove(ID)
		self.Actuators[ID] = Actuator(255)

	def send(self, data) -> None:
		if self._serial is not None:
			self._serial.write(data)

	def receive(self) -> list:
		if self._serial is not None:
			len = self._serial.inWaiting()
			data = self._serial.read(len)
			return list(data)
		return []

	def pass2buffer(self, data):
		for b in data:
			self.cb.write(b)

	def AutoScan(self) -> None:
		alive = []
		for i in range(255):
			self.addActuator(i)
			self.Timestamps[i] = 0
			self.send(self.Actuators[i].Ping())
			time.sleep(0.003)
			recv = self.receive()
			self.pass2buffer(recv)


		self.findPackage()

		for i in range(len(self.Timestamps)):
			if self.Timestamps[i] != 0:
				alive.append(i)

		self.ActList = alive
		return alive

#import random 
#m = Master(4096, '/dev/ttyACM2')
#print(m.AutoScan())
#for i in m.ActList:
#	new_id = random.randint(0,254)
#	dummy = Actuator(new_id)
#	m.send(m.Actuators[i].Write(dummy, [Parameters.deviceId]))
#	m.send(m.Actuators[new_id].ROMWrite())
#	m.send(m.Actuators[new_id].Reboot())
#print(m.AutoScan())