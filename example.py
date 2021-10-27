from actuator import *
import copy

m = Master(4096, "/dev/cu.usbmodem103", baudrate=115200)

print(m.AutoScan())

#Print last reply timestamps of actuators on the bus
for actuator in m.ActList:
	m.send(m.Actuators[actuator].Ping())
	m.pass2buffer(m.receive())
	m.findPackage()
	print(m.Timestamps[m.Actuators[actuator].Configuration.data.devID.data])

for actuator in m.ActList:
	act = Actuator(255) #temporary actuator object
	act.Configuration.data.baudRate.data = 57600
	m.send(m.Actuators[actuator].Write(act, [Parameters.baudrate]))
