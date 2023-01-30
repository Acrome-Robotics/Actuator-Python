import sys
import actuator
import struct
import socket
import concurrent.futures as cf
import queue
from actuator_types import *
import traceback

q = queue.Queue()


def DumpObjects(Actuator: actuator.Actuator):
	obj = bytearray()
	obj.extend(struct.pack("!f", float(Actuator.Configuration.data.devID.data)))
	st = str()
	for param in Actuator.Indexes[5:-1]:
		#Add actual value to array
		if isinstance(param[0].data, list):
			for data in param[0].data:
				obj.extend(struct.pack("!f", float(data.data)))
		else:
			obj.extend(struct.pack("!f", float(param[0].data)))
	return obj

def LoadObject(Actuator: actuator.Actuator, data_list):
	i = 5
	j = 0
	while i < Parameters.READ_ONLY_INDEX: #Iterate until last writable parameters
		Actuator.Indexes[i][0].data = data_list[j]
		i += 1
		j += 1

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

	def ReturnActuator(self, Actuator: actuator.Actuator):
		data = b'\x88' + DumpObjects(Actuator) #DUMP ACTUATOR
		return data

	def ReturnList(self, master: actuator.Master):
		data = b'\x99' + bytearray(master.ActList) #LIST ACTUATORS
		return data

def loop_master(master: actuator.Master):
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

def loop_udp(server:Server, master: actuator.Master):
	while True:
		data, client = server.receive()
		data = list(data)
		if data[0] == 0x55: #SCAN
			master.AutoScan()
		elif data[0] == 0x66: #LIST
			server.send(server.ReturnList(master))
		elif data[0] == 0x77: #UPDATE
			if data[1] == actuator.Actuator._commandLUT['Ping']:
				q.put(master.Actuators[data[2]].Ping())
			elif data[1] == actuator.Actuator._commandLUT['Read']:
				q.put(master.Actuators[data[2]].Read(data[3:], full=True))
			elif data[1] == actuator.Actuator._commandLUT['Write']:
				dummy_act = actuator.Actuator(data[2])
				data_list = struct.unpack('!IBBBBBHHHHBfffffffffffffffiIIfffB',bytes(data[3:]))
				print(data_list)
				LoadObject(dummy_act, data_list)
				q.put(master.Actuators[data[2]].Write(dummy_act))
			elif data[1] == actuator.Actuator._commandLUT['ROMWrite']:
				q.put(master.Actuators[data[2]].ROMWrite())
			elif data[1] == actuator.Actuator._commandLUT['Reboot']:
				q.put(master.Actuators[data[2]].Reboot())
			elif data[1] == actuator.Actuator._commandLUT['FactoryReset']:
				q.put(master.Actuators[data[2]].FactoryReset())
			elif data[1] == 0x44: #TIMESTAMP REQ
				server.send(struct.pack("!ff", float(data[2]), m.Timestamps[data[2]]))
			elif data[1] == 0x77: #DUMP REQ
				server.send(DumpObjects(master.Actuators[data[2]]))

try:
	serial_name = sys.argv[1]
	serial_baud = sys.argv[2]
except IndexError:
	print('Please provide serial port and baudrate in commandline arguments')
except Exception as exp:
	raise exp

s = Server(8000)
m = actuator.Master(4096, serial_name, serial_baud)

m.AutoScan()

with cf.ThreadPoolExecutor(max_workers=2) as executor:
	s_exec = executor.submit(loop_udp, s, m)
	m_exec = executor.submit(loop_master, m)

	try:
		data = s_exec.result()
	except Exception:
		print('UDP server generated an exception: %s' % (traceback.format_exc()))

	try:
		data = m_exec.result()
	except Exception:
		print('Master daemon generated an exception: %s' % (traceback.format_exc()))