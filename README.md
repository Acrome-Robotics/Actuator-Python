# Overview

This library provides easy-to-use Python modules and methods for interfacing with Acrome Smart Motor Driver products.

## Installation

## Usage

## Methods

- ### Red Class

- ### Master Class

  - #### `__init__(self, portname, baudrate=115200)`

    **`Return:`** *None*

    This is the initializer for Master class which controls the serial bus.

    `portname` argument is the serial/COM port of the host computer which is connected to the Acrome Smart Motor Drivers via Mastercard.

    `baudrate` argument specifies the baudrate of the serial port. User may change this value to something between 3.053 KBits/s and 12.5 MBits/s. However, it is up to the user to select a value which is supported by the user's host computer.

  - #### `update_driver_baudrate(self, id: int, br: int):`

    **`Return:`** *None*

    This method updates the baudrate of the driver, saves it to EEPROM and resets the driver board. Once the board is up again, the new baudrate is applied.

    `id` argument is the device ID of the connected driver.

    `br` argument is the user entered baudrate value. This value must be between 3.053 KBits/s and 12.5 MBits/s.

  - #### `update_master_baudrate(self, br: int):`

    **`Return:`** *None*

    This method updates the baudrate of the host computer's serial port and should be called after changing the baudrate of the driver board to sustain connection.

    `br` argument is the user entered baudrate value. This value must be between 3.053 KBits/s and 12.5 MBits/s.

  - #### `attach(self, driver: Red):`

    **`Return:`** *None*

    This method attaches an instance of Red class to the master. If a device ID is not attached to the master beforehand, methods of the master class will not work on the given device ID.

    `driver` argument is an instance of the Red class. Argument must be an instance with a valid device ID.


  - #### `detach(self, id: int):`

    **`Return:`** *None*

    This method removes the driver with the given device ID from the master. Any future action to the removed device ID will fail unless it is re-attached.

  - #### `set_variables(self, id: int, idx_val_pairs=[], ack=False)`

    **`Return:`** *List of the acknowledged variables or None*

    This method updates the variables of the driver board with respect to given index/value pairs.

    `id` argument is the device ID of the connected driver.

    `idx_val_pairs` argument is a list, consisting of lists of parameter indexes and their value correspondents.

  - #### `get_variables(self, id: int, index_list: list)`

    **`Return:`** *List of the read variables or None*

    This method reads the variables of the driver board with respect to given index list.

    `id` argument is the device ID of the connected driver.

    `index_list` argument is a list with every element is a parameter index intended to read.

  - #### `set_variables_sync(self, index: Index, id_val_pairs=[])`

    **`Return:`** *List of the read variables or None*

    This method updates a specific variable of the  multiple driver boards at once.

    `index` argument is the parameter to be updated.

    `id_val_pairs` argument is a list, consisting of lists of device IDs and the desired parameter value correspondents.

  - #### `scan(self)`

    **`Return:`** *List of the connected driver device IDs.*

    This method scans the serial port, detects and returns the connected drivers.

  - #### `reboot(self, id: int)`

    **`Return:`** *None*

    This method reboots the driver with given ID. Any runtime parameter or configuration which is not saved to EEPROM is lost after a reboot. EEPROM retains itself.

    `id` argument is the device ID of the connected driver.

  - #### `factory_reset(self, id: int)`

    **`Return:`** *None*

    This method clears the EEPROM config of the driver and restores it to factory defaults.
    
    `id` argument is the device ID of the connected driver.

  - #### `eeprom_write(self, id: int, ack=False)`

    **`Return:`** *None*

    This method clears the EEPROM config of the driver and restores it to factory defaults.
    
    `id` argument is the device ID of the connected driver.

  - #### `ping(self, id: int)`

    **`Return:`** *True or False*

    This method sends a ping package to the driver and returns `True` if it receives an acknowledge otherwise `False`.
    
    `id` argument is the device ID of the connected driver.

  - #### `reset_encoder(self, id: int)`

    **`Return:`** *None*
    
    This method resets the encoder counter to zero.

    `id` argument is the device ID of the connected driver.

  - #### `scan_sensors(self, id: int)`

    **`Return:`** *List of connected sensors*
    
    This method scans and returns the sensor IDs which are currently connected to a driver.

    `id` argument is the device ID of the connected driver.

  - #### `enter_bootloader(self, id: int)`

    **`Return:`** *None*
    
    This method puts the driver into bootloader. After a call to this function, firmware of the driver can be updated with a valid binary or hex file. To exit the bootloader, unplug - plug the driver from power or press the reset button.

    `id` argument is the device ID of the connected driver.

  - #### `get_driver_info(self, id: int)`

    **`Return:`** *Dictionary containing version info*
    
    This method reads the hardware and software versions of the driver and returns as a dictionary.

    `id` argument is the device ID of the connected driver.
    
  - #### `update_driver_id(self, id: int, id_new: int)`

    **`Return:`** *None*
    
    This method updates the device ID of the driver temporarily. `eeprom_write(self, id:int)` method must be called to register the new device ID.

    `id` argument is the device ID of the connected driver.

    `id_new` argument is the new intended device ID of the connected driver.

  - #### `enable_torque(self, id: int, en: bool)`

    **`Return:`** *None*

    This method enables or disables power to the motor which is connected to the driver.

    `id` argument is the device ID of the connected driver.

    `en` argument is a boolean. `True` enables the torque while False `disables`.

  - #### `pid_tuner(self, id: int)`

    **`Return:`** *None*

    This method starts a PID tuning process. Shaft CPR and RPM values **must** be configured beforehand. If CPR and RPM values are not configured, motors will not spin.

    `id` argument is the device ID of the connected driver.

  - #### `set_operation_mode(self, id: int, mode: OperationMode)`

    **`Return:`** *None*

    This method sets the operation mode of the driver. Operation mode may be one of the following: `OperationMode.PWM`, `OperationMode.Position`, `OperationMode.Velocity`, `OperationMode.Torque`.

    `id` argument is the device ID of the connected driver.

  - #### `get_operation_mode(self, id: int)`

    **`Return:`** *Operation mode of the driver*

    This method gets the current operation mode from the driver.

    `id` argument is the device ID of the connected driver.

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

  - #### `set_user_indicator(self, id: int)`

    **`Return:`** *None*

    This method sets the user indicator color on the RGB LED for 5 seconds. The user indicator color is cyan.

    `id` argument is the device ID of the connected driver.

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


  - #### `set_torque_limit(self, id: int, tl: int)`

    **`Return:`** *None*

    This method sets the torque limit of the driver in terms of milliamps (mA).

    `id` argument is the device ID of the connected driver.

    `tl` argument is the new torque limit (mA).


  - #### `get_torque_limit(self, id: int)`

    **`Return:`** *Torque limit (mA)*

    This method gets the torque limit from the driver in terms of milliamps (mA).

    `id` argument is the device ID of the connected driver.

  - #### `set_velocity_limit(self, id: int, vl: int)`

    **`Return:`** *None*

    This method sets the velocity limit for the motor output shaft in terms of RPM. The velocity limit applies only in velocity mode. Default velocity limit is 65535.

    `id` argument is the device ID of the connected driver.

    `vl` argument is the new velocity limit (RPM).

  - #### `get_velocity_limit(self, id: int)`

    **`Return:`** *Velocity limit*

    This method gets the velocity limit from the driver in terms of RPM.

    `id` argument is the device ID of the connected driver.

