from smd.red import*
import osModules

#id = 101
port = osModules.USB_serial_port()
print(port)
m = Master(port, 115200)

m.attach(Red(0))

print(m.get_driver_info(0))

print(m.scan_modules(0))

input('enter to start.')


i = 0
while True:
    print("button 1: " , m.get_button(0,1))
    print("button 3: " , m.get_button(0,3))
    print("button 5: " , m.get_button(0,5))
    print("rgb 1: " , i)
    m.set_rgb(0,1,(i==0)*255,(i==1)*255,(i==2)*255)
    print("rgb 2: " , i)
    m.set_rgb(0,2,(i==0)*255,(i==1)*255,(i==2)*255)
    print("rgb 5: ", i)
    m.set_rgb(0,5,(i==0)*255,(i==1)*255,(i==2)*255)

    i+=1
    if i==3:
        i=0

        