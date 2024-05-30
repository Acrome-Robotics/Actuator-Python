from smd.red import*
import osModules





id = 0
port = osModules.USB_serial_port()
print(port)
m = Master(port, 115200)

m.attach(Red(0))

print(m.get_driver_info(0))


print(m.scan_modules(0))

#print(m.get_variables(0, [Index.connected_bitfield]))

'''
m.set_operation_mode(0, OperationMode.Position)
m.enable_torque(0, True)
'''

'''
m.goTo(0, 40000)

'''