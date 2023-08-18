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

    ``id` argument is the device ID of the connected driver.

