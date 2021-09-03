from actuator import *
import copy

m = Master(4096, "/dev/ttyACM0")

m.AutoScan()

#Print last reply timestamps of actuators on the bus
for actuator in m.ActList:
	m.send(actuator.Ping())
	m.pass2buffer(m.receive())
	m.findPackage()
	print(m.Timestamps[actuator.Configuration.data.devID.data])

#Set all actuators to position control mode

for actuator in m.ActList:
	act = Actuator(255) #temporary actuator object
	act.Configuration.data.operationMode.data = OperationModes.PositionControl
	m.send(actuator.Write(act, [Parameters.operationMode]))

for actuator in m.ActList:
	act = copy.deepcopy(actuator)
	act.PositionControl.data.proportionalGain.data = 0.1
	act.PositionControl.data.integralGain.data = 0
	act.PositionControl.data.derivativeGain.data = 0.015
	act.PositionControl.data.feedForward.data = 90
	m.send(actuator.Write(act)) #Alternative way to write

act = Actuator(Actuator.BATCH_ID) #Apply to all actuators

#Continious stepping motion
while True:
	act.PositionControl.data.setpoint.data += 100
	m.send(actuator.Write(act, [Parameters.posSetpoint]))
	time.sleep(1)