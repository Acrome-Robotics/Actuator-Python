### An Example of Autotune 
```python
from smd.red import *
import time

MASTER_PORT =  "/dev/ttyUSB0" #depending on operating system, port, etc. may vary depending on the
master = Master(MASTER_PORT) #creating master object

print(master.scan()) #prints ID list of connected SMDs

ID = master.attached()[0] #getting ID of first SMD from scanned ones. You can use directly ID = 0 if it has never been changed before.

master.set_shaft_rpm(ID,10000)  #rpm and cpr values are depend on the motor you use.
master.set_shaft_cpr(ID,64)
master.pid_tuner(ID)            #starts autotune for setting PID values of control algorithms
```
#### you can see the PID values after then autotune with code below. 
```python
from smd.red import *
import time

MASTER_PORT =  "/dev/ttyUSB0"
master = Master(MASTER_PORT) #creating master object
print(master.scan())
ID = 0 #ID of the SMD connected and autotuned.

print(master.get_control_parameters_position(ID))
print(master.get_control_parameters_velocity(ID))

```

### An Example of PWM Control
```python
from smd.red import *


MASTER_PORT =  "COM10"
master = Master(MASTER_PORT) #creating master object
print(master.scan())
ID = 0 

master.set_operation_mode(ID, 0)    #sets the operating mode to 0 represents PWM control mode.
master.set_duty_cycle(ID, 50)       #sets the duty cycle to 50 percent
master.enable_torque(ID, True)      #enables the motor torque to start rotating
```
### An Example of Position Control
```python
from smd.red import *

MASTER_PORT =  "COM10"
master = Master(MASTER_PORT) #creating master object
print(master.scan())
ID = 0 

master.set_shaft_rpm(ID, 10000)  #rpm and cpr values are depend on the motor you use.
master.set_shaft_cpr(ID, 64)
master.set_control_parameters_position(ID, 10, 0, 8) #SMD ID, Kp, Ki, Kd

master.set_operation_mode(ID, 1)    #sets the operating mode to 1 represents Position control mode.
master.enable_torque(ID, True)      #enables the motor torque to start rotating

while True:
    master.set_position(ID, 5000)   #sets the setpoint to 5000 encoder ticks.
    time.sleep(1.2)
    master.set_position(ID, 0)      #sets the setpoint to 0 encoder ticks. Motor goes to start
    time.sleep(1.2)

```
You should enter the PID values of Position Control Mode or just tune once the SMD at start. CPR and RPM values should be entered to SMD calculates the neseccary varaibles. If you don't then the motor cannot rotate.

### An Example of Velocity Control
```python
from smd.red import *

MASTER_PORT =  "COM10"
master = Master(MASTER_PORT) #creating master object
print(master.scan())
ID = 0 

master.set_shaft_rpm(ID,10000)  #rpm and cpr values are depend on the motor you use.
master.set_shaft_cpr(ID,64)
master.set_control_parameters_velocity(ID,10,1,0) #SMD ID, Kp, Ki, Kd

master.set_operation_mode(ID, 2)    #sets the operating mode to 2 represents Velocity control mode.
master.set_velocity(ID, 2000)       #sets the setpoint to 2000 RPM.   

master.enable_torque(ID, True)      #enables the motor torque to start rotating
```
You should enter the PID values of Position Control Mode or just tune once the SMD at start. CPR and RPM values should be entered to SMD calculates the neseccary varaibles. If you don't then the motor cannot rotate.

### An Example of Torque Control
```python
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
```
You must enter the PID values of the Torque Control Mode. Since Auto tune does not produce these values, you must set them yourself. If you do not do this, the motor cannot rotate properly.


