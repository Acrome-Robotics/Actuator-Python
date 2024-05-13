from smd.red import*
import osModules





id = 0
port = osModules.USB_serial_port()
print(port)
m = Master(port, 115200)

m.attach(Red(0))

modules = ["Button_1", "Buzzer_3", "Distance_1", "Pot_3", "IMU_1"]

m.set_connected_modules(0, modules)
