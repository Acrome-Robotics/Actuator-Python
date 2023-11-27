import serial.tools.list_ports
import platform

def whichOS():
    return platform.system()


def USB_serial_port():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        for port, desc, hwid in sorted(ports):
            #print(f"{port}: {desc} [{hwid}]")
            #print(type(port))
            if 'USB Serial Port' in desc:
                return port
    else:
        return None



