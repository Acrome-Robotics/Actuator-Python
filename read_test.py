# Continuous reading code

from actuator import *
import copy
import pandas as pd


def printAct(act: Actuator):
    actVals = [[(act.Configuration.data.baudRate.data), "Baudrate"],
    [(act.Configuration.data.operationMode.data), "Operation Mode"],
	[(act.Limits.data.temperatureLimit.data),"temperatureLimit"],
	[(act.Configuration.data.torqueEnable.data), "torqueEnable"],
	[(act.Configuration.data.autotunerEnable.data), "autotunerEnable"],
	[(act.Indicators.data.RGB.data), "RGB"],
	[(act.Limits.data.minVoltage.data), "minVoltage"],
	[(act.Limits.data.maxVoltage.data), "maxVoltage"],
	[(act.Limits.data.torqueLimit.data), "torqueLimit"],
	[(act.Limits.data.velocityLimit.data), "velocityLimit"],
	[(act.Autotuner.data.method.data), "autotunerMethod"],
	[(act.PositionControl.data.feedForward.data), "PositionControlfeedForward"],
	[(act.VelocityControl.data.feedForward.data), "VelocityControlfeedForward"],
	[(act.TorqueControl.data.feedForward.data), "TorqueControlfeedForward"],
	[(act.PositionControl.data.scalerGain.data), "PositionControlscalerGain"],
	[(act.PositionControl.data.proportionalGain.data), "PositionControlproportionalGain"],
	[(act.PositionControl.data.integralGain.data), "PositionControlintegralGain"],
	[(act.PositionControl.data.derivativeGain.data), "PositionControlderivativeGain"],
	[(act.VelocityControl.data.scalerGain.data), "VelocityControlscalerGain"],
	[(act.VelocityControl.data.proportionalGain.data), "VelocityControlproportionalGain"],
	[(act.VelocityControl.data.integralGain.data), "VelocityControlintegralGain"],
	[(act.VelocityControl.data.derivativeGain.data),"VelocityControlderivativeGain"],
	[(act.TorqueControl.data.scalerGain.data), "TorqueControlscalerGain"],
	[(act.TorqueControl.data.proportionalGain.data), "TorqueControlproportionalGain"],
	[(act.TorqueControl.data.integralGain.data), "TorqueControlintegralGain"],
	[(act.TorqueControl.data.derivativeGain.data), "TorqueControlderivativeGain"],
	[(act.Limits.data.homeOffset.data), "homeOffset"],
	[(act.Limits.data.minPosition.data), "minPosition"],
	[(act.Limits.data.maxPosition.data), "maxPosition"],
	[(act.PositionControl.data.setpoint.data), "PositionControlsetpoint"],
	[(act.TorqueControl.data.setpoint.data), "TorqueControlsetpoint"],
	[(act.VelocityControl.data.setpoint.data), "VelocityControlsetpoint"],
	[(act.Sensors.data.buzzerEnable.data), "buzzerEnable"],
	[(act.Telemetry.data.position.data), "position"],
	[(act.Telemetry.data.velocity.data), "velocity"],
	[(act.Telemetry.data.voltage.data), "voltage"],
	[(act.Telemetry.data.temperature.data), "temperature"],
	[(act.Telemetry.data.current.data),  "current"],
	[(act.Sensors.data.presentRoll.data), "presentRoll"],
	[(act.Sensors.data.presentPitch.data), "presentPitch"],
	[(act.Sensors.data.lightIntensity.data), "lightIntensity"],
	[(act.Sensors.data.buttonPressed.data), "buttonPressed"],
	[(act.Sensors.data.distance.data), "distance"],
	[(act.Sensors.data.joystickX.data), "joystickX"],
	[(act.Sensors.data.joystickY.data), "joystickY"],
	[(act.Sensors.data.joystickButton.data), "joystickButton"],
	[(act.Sensors.data.qtrR.data), "qtrR"],
	[(act.Sensors.data.qtrM.data), "qtrM"],
	[(act.Sensors.data.qtrL.data), "qtrL"],
	[(act.Configuration.data.modelNum.data), "modelNum"],
	[(act.Configuration.data.firmwareVersion.data), "firmwareVersion"],
	[(act.Telemetry.data.errorCount.data), "errorCount"]]

    datas = [actVal[0] for actVal in actVals]
    indexes = [actVal[1] for actVal in actVals]
    df = pd.DataFrame(data=datas, index=indexes)

    print(df)

master = Master(4096, '/dev/ttyUSB0', baudrate=115200)
master.AutoScan()

print()
print(f"Number of Actuator boards connected: {len(master.ActList)}")


# full package read from connected Actuator boards
if(len(master.ActList) == 0):
    raise ConnectionError("No Actuator boards detected. Check cable connections!")
print(master.ActList)

while 1:
    for act_id in master.ActList:
        master.send(master.Actuators[act_id].Read(full=True))
        time.sleep(0.05)
        master.pass2buffer(master.receive())
        master.findPackage()

    
    for act_id in master.ActList:
        printAct(master.Actuators[act_id])

    print()
