# Introduction
Actuator Python SDK allows you to manage multiple Actuator boards with Python3. This SDK handles protocol implementation of the Actuator Boards alongside a Master interface that holds multiple Actuators and controls serial port for best performance. SDK developed to enable async communication with Actuators.

# Classes and Methods
The SDK contains multiple classes not only for end-user but for internal use too. This type of classes and methods will not be covered in this documentation.
## Actuator Class

### `Variables`

Type structure of the Actuator object can be found on the source code. Since all of the variables are self-explanatory, no extra documentation added for now. All the variables of the Actuator objects are instances of the `var` class. The `var` class is just a simple wrapper with a single variable named data. The intension of this usage is mimmicking the pointer functionality in C/C++. Since the communication protocol of the Actuator boards have variable sized structure with selective read/write operations, hard coded conditional operations can have a negative impact on the maintainability of the SDK development. This choice comes with a trade-off between the difficulty of using and developing the SDK.

User should access all data in the Actuator objects like below:
```
act = Actuator(0)

act.Configuration.data.torqueEnable.data = 1

```

### `__init__(ID):`
**Parameters:**
* `ID:` Device ID of the Actuator Board

```
from actuator import *
myActuator = Actuator(0)

```

### `Ping():`
**Parameters:** None

**Returns:** list that contains ping package for the Actuator

This method is used for generating a ping package for the related Actuator. Ping packages are useful for checking Actuators on the bus.

```
ping_data = myActuator.Ping()

user_defined_serial_write_function(ping_data)
```

### `Read(params=[], full=False):`
**Parameters:**
* `params:` List of parameter indexes to be read.
* `full:` Request for full read. Default value is false.

**Returns:** list that contains read command package of given variables.

This method is used for generating a package for reading variables from the Actuator board.

When *full* parameter set to true, *params* is ignored and full package request is generated. In this configuration, the Actuator replies with a package that contains all variables.

When *full* parameter is set to false, method generates a package to read given list of parameter indexes. Valid indexes are defined in `Parameters` class and can be accessed as class members.

```
#Read all variables at once
read_pkg = myActuator.Read([],full=True)
user_defined_serial_write_function(read_pkg)

```

```
#Read present position, current and velocity only.
param_list = [Parameters.presentPosition, Parameters.presentVelocity, Parameters.presentCurrent]
read_pkg = myActuator.Read(param_list)

user_defined_serial_write_function(read_pkg)
```

### `Write(Act)`
**Parameters:**
* `Act`: An Actuator object with the desired parameter set.
* `param_list`: List of parameters to be updated.

**Returns:**
list that contains write command package of changed variables.

This method takes an object as the new state and compares with the actual Actuator. At the end of the comparison, a package that changes these variables will be generated. User can use the `copy` module to create a deep copy of the Actuator object, change desired parameters and pass to the module or can create a temporary Actuator object with a parameter list with elements as instances of `Parameters` class variables in *param_list*. When user pass a parameter list, only given parameters will be changed regardless of the passed object.

```
import copy

#Copy actual object
Act = copy.deepcopy(myActautor)

#Set torqueEnable
Act.Configuration.data.torqueEnable.data = 1

#Generate write package
write_pkg = myActuator.Write(Act)

#Send over serial
user_defined_serial_write_function(write_pkg)
```

```
#Create a temporary object
Act = Actuator(0)

#Set torqueEnable
Act.Configuration.data.torqueEnable.data = 1

#Generate write package
write_pkg = myActuator.Write(Act, [Parameters.torqueEnable])

#Send over serial
user_defined_serial_write_function(write_pkg)
```

### `Reboot()`
**Parameters:** None

**Returns:**
list that contains reboot command package.

This method generates a reboot command package to reboot the Actuator.

```
reboot_data = myActuator.Reboot()

user_defined_serial_write_function(reboot_data)
```

### `FactoryReset()`
**Parameters:** None

**Returns:**
list that contains factory reset command package.

This method generates a factory reset command package to take the Actuator back to the factory defaults.

```
fr_data = myActuator.FactoryReset()

user_defined_serial_write_function(fr_data)
```

### `ROMWrite()`
**Parameters:** None

**Returns:**
list that contains ROM write command package.

This method generates a ROM write command package to save parameters to the non-volatile memory.

```
romwrite_data = myActuator.ROMWrite()

user_defined_serial_write_function(romwrite_data)
```

### `parse(package)`
**Parameters:** package received from serial as a list

**Returns:** None

This method parses the received package and updates values of the Actuator object. This method does not check received package's integrity. For a safer communication, use the `Master` interface which is provided with this SDK.

```
#Read all variables at once
read_pkg = myActuator.Read([],full=True)
user_defined_serial_write_function(read_pkg)

#Receive reply from the bus
received_package = user_defined_serial_read()

#Parse received package
myActuator.parse(received_package)

print(myActuator.Telemetry.data.position.data)
```

## Master Class

### `__init__()`
**Parameters:**
* `size:` Size of buffer to be used for serial
* `portname:` Name of the serial port
* `baudrate:` Baudrate of the serial port. Default is 115200.
* `master_timeout:` Timeout value for Actuator bus in seconds. Default is 10ms.

**Returns:** None

Constructor of this class is responsible for configuring Circular Buffer for serial along with the serial port itself. User should provide a valid serial port name. Buffer size parameter must a power of 2. Recomended minimum value is 256. Recomended value is 4096 for general use.

```
m = Master(4096, '/dev/ttyUSB0', 115200, 0.01)
```


### `addActuator()`
**Parameters:**
* `ID:` Device ID of the Actuator Board which will be added.

**Returns:** None

This method, adds new Actuator to the list of the Master instance for further operations. All Actuator objects of the Master instance can be accessed via `Actuators` variable of the class. Index of the Actuator object is same as the ID. But user should be careful about accessing Actuator objects since `Actuators` variable holding empty cells too.

```

m.addActuator(96)

print(isinstance(m.Actuators[96], Actuator)) # Prints true.
print(isinstance(m.Actuators[196], Actuator)) # Prints false.

```

### `removeActuator()`
**Parameters:**
* `ID:` Device ID of the Actuator Board which will be removed.

**Returns:** None

This method, removes the Actuator with the given ID from the private list of the Master instance for further operations.

```
m.removeActuator(96)
```

### `send()`
**Parameters:**
* `data:` Data that will be sent over serial as bytes.

**Returns:** None

This method is a simple wrapper for serial write operations.

```
m.send(m.Actuators[96].Ping())
```


### `receive()`
**Parameters:** None

**Returns:** list

This method is a simple wrapper for serial read operations. Returns all available data on the bus as a list.

```
data = m.receive()
```

### `pass2buffer()`
**Parameters:**
* `data:` data came from serial bus.

**Returns:** None

This method passes incoming data to the internal Circular Buffer.

```
data = m.receive()
m.pass_to_buffer(data)
```


### `findPackage()`
**Parameters:** None

**Returns:** None

This method is used to process the buffer of the Master instance. When a valid package found on the buffer, the Master will update the relevant Actuator object(s).

```
data = m.receive()
m.pass_to_buffer(data)

m.findPackage()
```

### `AutoScan()`

**Parameters:** None

**Returns:** None

This method is for scanning the bus and attaching the Actuators on the bus to the Master instance. This automates and simplifies the initialization stage of the class.

```
m = Master(4096, '/dev/ttyUSB0', 115200, 0.01)
m.AutoScan() #This line scans and adds Actuators.
```