import math
import decimal
import time

from smd.red import *

def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)

timePoints = list(float_range(0, 4.18, '0.1'))

def pwm_f(x):
    final = 20*math.sin((1.5)*x)
    if final < 0:
        return final*(4/3)
    else:
        return final
    

def pwm2_f(x):
    final = 80*math.sin((1.5)*x)
    return final


MASTER_PORT =  "COM12"
master = Master(MASTER_PORT) #creating master object
#print(master.scan())
ID  = 0
ID1 = 1
ID2 = 2

master.attach(Red(ID))
master.attach(Red(ID1))
master.attach(Red(ID2))

master.set_operation_mode(ID2, 0)    #sets the operating mode to 0 represents PWM control mode.
master.enable_torque(ID2, True)      #enables the motor torque to start rotating

master.set_operation_mode(ID1, 0)    #sets the operating mode to 0 represents PWM control mode.
master.enable_torque(ID1, True)      #enables the motor torque to start rotating

master.set_operation_mode(ID, 0)    #sets the operating mode to 0 represents PWM control mode.
master.enable_torque(ID, True)      #enables the motor torque to start rotating

def pwmSinTask(id):
    while True:
        for t in timePoints :
            master.set_duty_cycle(id, pwm_f(t))
            time.sleep(0.1)

def pwmSinTaskto80(id):
    while True:
        for t in timePoints :
            master.set_duty_cycle(id, pwm2_f(t))
            time.sleep(0.1)


