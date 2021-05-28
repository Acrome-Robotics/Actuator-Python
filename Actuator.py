from crccheck.crc import Crc32Mpeg2 as CRC32
import time
from ActuatorTypes import *
from ctypes import *
import struct
import serial
import socket
import concurrent.futures as cf
import queue

q = queue.Queue()

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

class Actuator():

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
		self.ExternalPort = var(ExternalPort())
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
			[(self.ExternalPort.data.portMode), 1, c_uint8],
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
			[(self.ExternalPort.data.portData), 4, c_uint32],
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
		return self.header.data.to_bytes(1,'little') +\
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

	def Write(self, Act):
		params = []
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
				updating.extend(struct.pack("!f", Act.Indexes[param][0].data))
			elif Act.Indexes[param][2] in [c_uint8, c_ubyte, c_char]:
				updating.extend(struct.pack("!B", Act.Indexes[param][0].data & 0xFF))
			elif Act.Indexes[param][2] == c_uint16:
				updating.extend(struct.pack("!H", Act.Indexes[param][0].data & 0xFFFF))
			elif Act.Indexes[param][2] == c_uint32:
				updating.extend(struct.pack("!I", Act.Indexes[param][0].data & 0xFFFFFFFF))
			elif Act.Indexes[param][2] == c_int32:
				updating.extend(struct.pack("!i", Act.Indexes[param][0].data & 0xFFFFFFFF))

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

	def DumpObjects(self):
		obj = bytearray()
		obj.extend(struct.pack("!B", self.Configuration.data.devID.data))
		st = str()
		for param in self.Indexes[5:34]:
			#Add actual value to array
			if param[2] == c_float:
				obj.extend(struct.pack("!f", param[0].data))
			elif param[2] in [c_uint8, c_ubyte, c_char]:
				obj.extend(struct.pack("!B", param[0].data))
			elif param[2] == c_uint16:
				obj.extend(struct.pack("!H", param[0].data))
			elif param[2] == c_uint32:
				obj.extend(struct.pack("!I", param[0].data))
			elif param[2] == c_int32:
				obj.extend(struct.pack("!i", param[0].data))

		return obj

	def LoadObject(self, data_list):
		for i in len(self.Indexes):
			self.Indexes[i][0].data = data_list[i]

	#Parse package which is already checked against CRC and package integrity
	def parse(self, package):
		cmds = self.__class__._commandLUT

		if package[3] == cmds['Read']:
			i = 5
			while i < (len(package) - 4):

				#Floats
				if self.Indexes[package[i]][2] == c_float:
					self.Indexes[package[i]][0].data = struct.unpack('<f', bytes(package[i+1:i+1+self.Indexes[package[i]][1]]))[0]
					i += self.Indexes[package[i]][1]
				#Integers
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
	def __init__(self, size, serial):
		self.cb = CircularBuffer(size)
		self.ActList = []
		self.Actuators = [Actuator(255)] * 255
		self.Timestamps = [0] * 255
		self._serial = serial

	def addActuator(self, ID):
		if ID not in self.ActList:
			self.ActList.append(ID)
			self.Actuators[ID] = Actuator(ID)

	def findPackage(self):

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

	def removeActuator(self, ID):
		self.ActList.remove(ID)
		self.Actuators[ID] = Actuator(255)

	def send(self, data):
		if self._serial is not None:
			self._serial.write(data)

	def receive(self, expected_bytes=0):
		if self._serial is not None:
			data = self._serial.read(256)
			return list(data)

	def AutoScan(self):
		alive = []
		for i in range(255):
			self.addActuator(i)
			self.Timestamps[i] = 0
			self.send(self.Actuators[i].Ping())
			time.sleep(0.003)
			recv = self.receive()
			for b in recv:
				self.cb.write(b)

		self.findPackage()

		for i in range(len(self.Timestamps)):
			if self.Timestamps[i] != 0:
				alive.append(i)

		self.ActList = alive
		return alive

class Server():
	IP = '127.0.0.1'
	bufferSize = 4096
	def __init__(self, port):
		self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.port = port
		self.socket.bind((self.IP, self.port))
		self.client = None

	def receive(self):
		data, address = self.socket.recvfrom(self.bufferSize)
		self.client = address
		return (data, address)

	def send(self, data, client = None):
		if client is not None:
			self.socket.sendto(data, client)

		if self.client is not None:
			self.socket.sendto(data, self.client)

	def ReturnActuator(self, Actuator):
		data = b'\x88' + Actuator.DumpObjects() #DUMP ACTUATOR
		return data

	def ReturnList(self, master):
		data = b'\x99' + bytearray(master.ActList) #LIST ACTUATORS
		return data

def loop_master(master):
	while True:
		data = None
		try:
			pass
			data = q.get_nowait()
		except Exception:
			pass

		if data is not None:
			master.send(data)
		data = master.receive()
		if len(data) > 0:
			for i in list(data):
				master.cb.write(i&0xFF)
		master.findPackage()

def loop_udp(server, master):
	while True:
		data, client = server.receive()
		data = list(data)
		if data[0] == 0x55: #SCAN
			master.AutoScan()
		elif data[0] == 0x66: #LIST
			server.send(server.ReturnList(master))
		elif data[0] == 0x77: #UPDATE
			if data[1] == Actuator._commandLUT['Ping']:
				q.put(master.Actuators[data[2]].Ping())
			elif data[1] == Actuator._commandLUT['Read']:
				q.put(master.Actuators[data[2]].Read(data[3:]))
			elif data[1] == Actuator._commandLUT['Write']:
				data_list = struct.unpack('!B!I!B!B!B!B!B!H!H!H!H!f!f!f!f!f!f!f!f!f!f!f!f!i!I!I!I!f!f!f', data[3:])
				master.Actuators[data[2]].LoadObject(data_list)
			elif data[1] == Actuator._commandLUT['ROMWrite']:
				q.put(master.Actuators[data[2]].ROMWrite())
			elif data[1] == Actuator._commandLUT['Reboot']:
				q.put(master.Actuators[data[2]].Reboot())
			elif data[1] == Actuator._commandLUT['FactoryReset']:
				q.put(master.Actuators[data[2]].FactoryReset())
			elif data[1] == 0x44: #TIMESTAMP REQ
				struct.pack("!B!f", data[2], m.Timestamps[data[2]])
			elif data[1] == 0x77: #DUMP REQ
				server.send(master.Actuators[data[2]].DumpObjects())

ser = None
#ser = serial.Serial(port='/ttyACM0', baudrate = 115200, timeout=0.25)
s = Server(8000)
m = Master(4096, ser)

m.AutoScan()
executor = cf.ThreadPoolExecutor(max_workers=2)
executor.submit(loop_udp, s, m)
executor.submit(loop_master, m)
