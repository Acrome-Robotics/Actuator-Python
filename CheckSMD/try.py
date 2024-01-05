from smd.red import*
import osModules





id = 101
port = osModules.USB_serial_port()
m = Master(port, 115200)

'''
print(m.scan())

'''
m.attach(Red(id))

m.enable_torque(id, True)

while 1:
    print(m.get_position(id))
    m.set_duty_cycle(id , 50)
    time.sleep(2)
    print(m.get_position(id))
    m.set_duty_cycle(id , -50)
    



"""
print(m.get_shaft_cpr(id))
print(m.get_shaft_rpm(id))


if m.get_shaft_cpr(id)[0]==(cpr):
        if m.get_shaft_rpm(id)[0]==(rpm):
            print("yes")

"""



