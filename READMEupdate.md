# Python Library

# Overview
This library provides easy-to-use Python modules and methods for interfacing with Acrome Smart Motor Driver products.

Embrace the world of motor control with simplicity using our SMD Python Library. Designed specifically for controlling SMDs, this library provides a seamless experience no matter your skill level in how you control motors.

Whether your project requires basic speed adjustments or precise position control, quickly and easily leverage the flexibility of Python to effortlessly implement a wide variety of motor control strategies.

SMD Python Library takes your projects to the next level by offering seamless integration ith SMD Sensor modules. With this library, you can increase the functionality and efficiency of your project bwy effortlessly collecting data from SMD sensor modules via SMD.

Develop your projects with "Acrome Smart Motor Drivers" and a computer that can run your Python code.

You can reach the Acrome Smart Motors Drivers documentation [here](https://acrome-smd.readthedocs.io/en/latest/getting-started.html).

# Installation
To use [Acrome Smart Motor Drivers](https://acrome.net/product/smart-motor-drivers) with python library, follow the installation steps below. Library is compatible with Python 3.x and can be installed on both Windows and Linux systems.

### Prerequisites

Before you begin, make sure you have the following prerequisites:

- Python 3.x: [Python Official Website](https://www.python.org/downloads/)

### Installation                

#### Windows

1. Open a Command Prompt with administrative privileges.

2. Install SMD library using `pip` (Python package manager) by running the following command:

  ```shell
  pip install acrome-smd
  ```

3. Wait for the installation to complete. Pip willmnmnmnmn automatically download and install the library along with any required dependencies.

#### Linux
1. Open a terminal.

2. Install SMD library using pip (Python package manager) by running the following command:

  ```shell
  pip install acrome-smd
  ```

3. Wait for the installation to complete. Pip will automatically download and install SMD Library along with any required dependencies.

### Verification
To verify that SMD library has been successfully installed, open a Python interpreter and run the following command:

```python
import smd
import smd.red
```
If no errors are raised, the installation was successful.

### Upgrading
To upgrade SMD Library to the latest version, you can use the following pip command:

  ```shell
  pip install acrome-smd
  ```
# Usage
Import the BLABLA Library:
First, import the BLABLA library at the beginning of your Python script:

```python
from smd.red import *
```
### Initialize SMD:

Create an instance of the BLA class by initializing it with the appropriate settings. This instance represents your BLABLA motor driver and allows you to control it.

````python
ID = 0  # Set the ID of your SMART MOTOR DRIVER
SerialPort = '/dev/ttyUSB0'  # Replace with your specific serial port ( for ex 'COM3'.)
baudrate = 115200  # Set the baud rate for serial communication

myMaster = Master(SerialPort , baudrate) #create a master object
print(master.scan()) #prints ID list of connected SMDs


from smd.red import *
import time

MASTER_PORT =  "/dev/ttyUSB0" #depending on operating system, port, etc. may vary depending on the
master = Master(MASTER_PORT) #creating master object

print(master.scan()) #prints ID list of connected SMDs

ID = master.attached()[0] #getting ID of first SMD from scanned ones.
#ID = 0 You can use directly this if it has never been changed before.
````

Configure SMD:

````python
#rpm and cpr values are depend on the motor you use.
master.set_shaft_rpm(ID,10000) 
master.set_shaft_cpr(ID,64)

#starts autotune for setting PID values of control algorithms
master.pid_tuner(ID)            
````
You can configure and use the **SMD**  using specific methods belonging to the master class, just like in the code above.

You can access all sample codes from [here](https:asıodasdasd.com) .
Please read full documentation to use all features of a **SMD** 


# Brushed DC Motor Control and Control Modes
The SMD Red has 4 control modes:

- **PWM Control:** This mode provides power to a brushed DC motor using PWM signals.

- **Position Control:** In this mode, the brushed motor moves to the desired positions using information from the encoder.

- **Velocity Control:** This mode ensures that the motor rotates at the desired speed using data from the encoder.

- **Torque Control:** This mode allows the motor to apply a specific torque by drawing the desired current.

Except for the *PWM Control mode*, all of these control modes operate with PID control. Therefore, it is essential to configure the PID values before starting the motors in these control modes. Without proper PID tuning, the motors may not work at all or may not perform as desired. You can find the necessary information for setting PID values in the [PID Tune](#pid-tune) section of the documentation.

#### Control Methods

Regardless of which control mode you choose to use, there are two essential methods that you need to be aware of. One is the `set_operation_mode()` method, which allows you to select the motor control mode you want to use. The other is `enable_torque()`, which enables or disables the motor rotation.

- #### `set_operation_mode(self, id: int, mode: OperationMode)`

    **`Return:`** *None*

    This method sets the operation mode of the driver. Operation mode may be one of the following:
    - `OperationMode.PWM`, 
    - `OperationMode.Position`,
    - `OperationMode.Velocity`,
    - `OperationMode.Torque`.

    `id` argument is the device ID of the connected driver.

- #### `enable_torque(self, id: int, en: bool)`

    **`Return:`** *None*

    This method enables or disables power to the motor which is connected to the driver.

    `id` argument is the device ID of the connected driver.

    `en` argument is a boolean. `True` enables the torque while False `disables`.




### PWM Control
- ####  `set_duty_cycle(self, id: int, pct: float):`

    **`Return:`** *None*

    This method sets the duty cycle to the motor for PWM control mode in terms of percentage. Negative values will change the motor direction.

    `id` argument is the device ID of the driver.

    `id` argument is the duty cycle percentage.
#### An Example of PWM Control
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
### Position Control
  - #### `set_position_limits(self, id: int, plmin: int, plmax: int)`

    **`Return:`** *None*

    This method sets the position limits of the motor in terms of encoder ticks. Default for min is -2,147,483,648 and for max is 2,147,483,647. The torque is disabled if the value is exceeded so a tolerence factor should be taken into consideration when setting these values.

    `id` argument is the device ID of the connected driver.

    `plmin` argument is the minimum position limit.

    `plmax` argument is the maximum position limit.

  - #### `get_position_limits(self, id: int)`

    **`Return:`** *Min and max position limits*

    This method gets the position limits of the motor in terms of encoder ticks.

    `id` argument is the device ID of the connected driver.

    `plmin` argument is the minimum position limit.

    `plmax` argument is the maximum position limit.

  - ####  `set_position(self, id: int, sp: int)`

    **`Return:`** *None*

      This method sets the desired setpoint for the position control in terms of encoder ticks.

      `id` argument is the device ID of the driver.

      `sp` argument is the position control setpoint.


  - ####  `get_position(self, id: int)`

    **`Return:`** *Current position of the motor shaft*

      This method gets the current position of the motor from the driver in terms of encoder ticks.

      `id` argument is the device ID of the driver.

#### An Example of Position Control

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

### Velocity Control
- #### `set_velocity_limit(self, id: int, vl: int)`

    **`Return:`** *None*

    This method sets the velocity limit for the motor output shaft in terms of RPM. The velocity limit applies only in velocity mode. Default velocity limit is 65535.

    `id` argument is the device ID of the connected driver.

    `vl` argument is the new velocity limit (RPM).

- #### `get_velocity_limit(self, id: int)`

    **`Return:`** *Velocity limit*

    This method gets the velocity limit from the driver in terms of RPM.

    `id` argument is the device ID of the connected driver.
- ####  `set_velocity(self, id: int, sp: int)`

    **`Return:`** *None*

      This method sets the desired setpoint for the velocity control in terms of RPM.

      `id` argument is the device ID of the driver.


- ####  `get_velocity(self, id: int)`

    **`Return:`** *Current velocity of the motor shaft*

      This method gets the current velocity of the motor output shaft from the driver in terms of RPM.

      `id` argument is the device ID of the driver.

#### An Example of Velocity Control
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
### Torque Control
  - #### `set_torque_limit(self, id: int, tl: int)`

    **`Return:`** *None*

    This method sets the torque limit of the driver in terms of milliamps (mA).

    `id` argument is the device ID of the connected driver.

    `tl` argument is the new torque limit (mA).


  - #### `get_torque_limit(self, id: int)`

    **`Return:`** *Torque limit (mA)*

    This method gets the torque limit from the driver in terms of milliamps (mA).

    `id` argument is the device ID of the connected driver.

   - ####  `set_torque(self, id: int, sp: int)`

        **`Return:`** *None*

        This method sets the desired setpoint for the torque control in terms of milliamps (mA).

        `id` argument is the device ID of the driver.


   - ####  `get_torque(self, id: int)`

        **`Return:`** *Current drawn from the motor (mA)*

        This method gets the current drawn from the motor from the driver in terms of milliamps (mA).

        `id` argument is the device ID of the driver.

#### An Example of Torque Control
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
**_You must enter the PID values of the Torque Control Mode. Since Auto tune does not produce these values, you must set them yourself._** If you do not do this, the motor cannot rotate properly.

# PID Tune and Setting Control Parameters

The control modes on the SMD device operate with PID control. Therefore, correctly tuning the P, I, and D constants is crucial for accurate control. The device features an autotune capability to automatically set these values. Alternatively, users can manually input these values if desired.

### Autotune
To utilize the autotune feature on the device, it's essential to ensure that the motor is in a freely rotatable position. This is because the card continuously rotates the motor during the autotuning process.

Following this, the next step is to input the motor's CPR (Counts Per Revolution) and RPM (Revolutions Per Minute) values into the card using the provided methods below. Failing to do this accurately may result in incorrect calculations.

  - #### `set_shaft_cpr(self, id: int, cpr: float)`

    **`Return:`** *None*

    This method sets the count per revolution (CPR) of the motor output shaft.

    `id` argument is the device ID of the connected driver.

    `cpr` argument is the CPR value of the output shaft

  - #### `set_shaft_rpm(self, id: int, rpm: float)`

    **`Return:`** *None*

    This method sets the revolution per minute (RPM) value of the output shaft at 12V rating.

    `id` argument is the device ID of the connected driver.

    `rpm` argument is the RPM value of the output shaft at 12V

After completing these steps, you should initiate the tuning process using the ``pid_tuner()`` method. Please note that immediately after calling this method, the motors will start rotating with varying speeds.

  - #### `pid_tuner(self, id: int)`

    **`Return:`** *None*

    This method starts a PID tuning process. Shaft CPR and RPM values **must** be configured beforehand. If CPR and RPM values are not configured, motors will not spin.

    `id` argument is the device ID of the connected driver.

Once the ``pid_tuner()`` method is initiated, the state of the torque (whether it's enabled or not) does not affect motor operation. There is no need to use the ``enable_torque()`` function.

#### An Example of Autotune 
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

### Setting PID Values
Manual input of the necessary constants for PID control is also possible. For this, separate P, I, and D constants should be configured for each control mode. Please note that each mode utilizes its own set of constants to control the motor. There are dedicated methods for configuring these constants for each control mode.

- ####  `set_control_parameters_position(self, id: int, p=None, i=None, d=None, db=None, ff=None, ol=None)`

    **`Return:`** *None*

      This method sets the control block parameters for position control mode.
      Only assigned parameters are written, `None`'s are ignored. The default
      max output limit is 950.

      `id` argument is the device ID of the driver.

      `p` argument is the the proportional gain. Defaults to None.

      `i` argument is the integral gain. Defaults to None.

      `d` argument is the derivative gain. Defaults to None.

      `db` argument is the deadband (of the setpoint type) value. Defaults to None.

      `ff` argument is the feedforward value. Defaults to None.

      `ol` argument is the maximum output limit. Defaults to None.


- ####  `set_control_parameters_velocity(self, id: int, p=None, i=None, d=None, db=None, ff=None, ol=None)`

    **`Return:`** *None*

      This method sets the control block parameters for velocity control mode.
        Only assigned parameters are written, `None`'s are ignored. The default
        max output limit is 950.

      `id` argument is the device ID of the driver.

      `p` argument is the the proportional gain. Defaults to None.

      `i` argument is the integral gain. Defaults to None.

      `d` argument is the derivative gain. Defaults to None.

      `db` argument is the deadband (of the setpoint type) value. Defaults to None.

      `ff` argument is the feedforward value. Defaults to None.

      `ol` argument is the maximum output limit. Defaults to None.
- ####  `set_control_parameters_torque(self, id: int, p=None, i=None, d=None, db=None, ff=None, ol=None)`

    **`Return:`** *None*

      This method sets the control block parameters for torque control mode.
        Only assigned parameters are written, `None`'s are ignored. The default
        max output limit is 950.

      `id` argument is the device ID of the driver.

      `p` argument is the the proportional gain. Defaults to None.

      `i` argument is the integral gain. Defaults to None.

      `d` argument is the derivative gain. Defaults to None.

      `db` argument is the deadband (of the setpoint type) value. Defaults to None.

      `ff` argument is the feedforward value. Defaults to None.

      `ol` argument is the maximum output limit. Defaults to None.

### Getting PID Values and Control values
The P, I, and D constants and other values entered for control modes can be obtained. This can be achieved by using the methods provided below.

- ####  `get_control_parameters_position(self, id: int)`

    **`Return:`** *Returns the list [P, I, D, Feedforward, Deadband, OutputLimit]*

    This method gets the position control block parameters.

    `id` argument is the device ID of the driver.

- ####  `get_control_parameters_velocity(self, id: int)`

    **`Return:`** *Returns the list [P, I, D, Feedforward, Deadband, OutputLimit]*

    This method gets the velocity control block parameters.

    `id` argument is the device ID of the driver.
  
- ####  `get_control_parameters_torque(self, id: int)`

    **`Return:`** *Returns the list [P, I, D, Feedforward, Deadband, OutputLimit]*

    This method gets the torque control block parameters.

    `id` argument is the device ID of the driver.

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


### Setting Control Limits 








# Sensor Modules
#### Seonsor Modules Basic
#####  Sensor 1
#####  Sensor 2
#####  Sensor ....


# All Methods

