from smd.red import *

MASTER_PORT =  "COM10"
master = Master(MASTER_PORT) #creating master object
print(master.scan())
ID = 0 

master.set_shaft_rpm(ID,10000)  #rpm and cpr values are depend on the motor you use.
master.set_shaft_cpr(ID,64)
master.set_control_parameters_torque(ID, 10, 0.1, 0) #SMD ID, Kp, Ki, Kd
#master.set_torque_limit(220)

master.set_operation_mode(ID, 3)    #sets the operating mode to 3 represents Torque control mode.
master.set_torque(ID, 80)          #sets the setpoint to 80 mili amps(mA).
master.enable_torque(ID, True)      #enables the motor torque to start rotating