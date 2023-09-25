from smd.red import *


MASTER_PORT =  "COM12"
master = Master(MASTER_PORT) #creating master object
#print(master.scan())
ID = 0
ID2 = 2 
master.attach(Red(ID))
master.attach(Red(ID2))

master.set_operation_mode(ID2, 0)    #sets the operating mode to 0 represents PWM control mode.
master.enable_torque(ID2, True)      #enables the motor torque to start rotating

master.set_operation_mode(ID, 0)    #sets the operating mode to 0 represents PWM control mode.
master.enable_torque(ID, True)      #enables the motor torque to start rotating
master.set_duty_cycle(ID, 80)

while True:
    master.set_duty_cycle(ID2, 30)
    time.sleep(1)
    master.set_duty_cycle(ID2, 0)
    time.sleep(1)
    master.set_duty_cycle(ID2, -40)
    time.sleep(1)






"""
while True:
    master.get_analog_port(ID)
    master.set_duty_cycle(ID, 40)       #sets the duty cycle to 50 percent
    time.sleep(2)
    master.set_duty_cycle(ID, -40)       #sets the duty cycle to 50 percent
    time.sleep(2)"""
