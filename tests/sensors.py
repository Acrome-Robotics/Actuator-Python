from smd.red import *

port = "COM12"
m = Master(port)


id = 2
m.attach(Red(id))

print(m.scan_sensors(id))

m.set_variables(id,[[Index.Servo_2, 50]])
