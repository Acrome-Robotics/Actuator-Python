import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Actuator import *

m.addActuator(0)
ActDummy = Actuator(0)
while True:
	#q.put(m.Actuators[0].Ping())
	ActDummy.Indicators.data.RGB.data += 1
	prt = []
	prt.append(m.Timestamps[0])
	prt.append(m.Actuators[0].Configuration.data.baudRate.data)
	prt.append(m.Actuators[0].Telemetry.data.current.data)
	prt.append(m.Actuators[0].Telemetry.data.errorCount.data)
	prt.append(m.Actuators[0].Telemetry.data.error.data)
	prt.append(m.Actuators[0].Indicators.data.RGB.data)
	print(prt)
	for act in m.ActList:
		q.put(m.Actuators[act].Write(ActDummy))
		q.put(m.Actuators[act].Read(full=True))
		time.sleep(0.02)
		q.put(m.Actuators[act].Ping())
		m.findPackage()

