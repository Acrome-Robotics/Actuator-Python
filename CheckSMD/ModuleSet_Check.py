from smd.red import*
from colorama import Fore, Style, init
from tabulate import tabulate
import os
from osModules import*

BUTTON_check	= False
LIGHT_check		= False
BUZZER_check	= False
JOYSTICK_check	= False
DISTANCE_check	= False
QTR_check	    = False
SERVO_check		= False
POT_check	    = False
RGB_check	    = False 
IMU_check		= False

operatingSystem = whichOS()
port = USB_serial_port()
m = Master(port)
m.attach(Red(0))
ID = 0      #connect to all IDs

modulesList = m.scan_modules(0)
print(modulesList)

modulesID = 1



try:
    if "Button_1" in modulesList:
        BUTTON_check = True
    
    if "Light_1" in modulesList:
        LIGHT_check = True

    if "Buzzer_1" in modulesList:
        BUZZER_check = True

    if "Joystick_1" in modulesList:
        JOYSTICK_check = True   

    if "Distance_1" in modulesList:
        DISTANCE_check = True

    if "QTR_1" in modulesList:
        QTR_check = True

    if "Servo_1" in modulesList:
        SERVO_check = True

    if "Pot_1" in modulesList:
        POT_check = True

    if "RGB_1" in modulesList:
        RGB_check = True

    if "IMU_1" in modulesList:
        IMU_check = True
except:
    pass

def colorize_boolean(value):
    return f"{Fore.GREEN}True{Style.RESET_ALL}" if value else f"{Fore.RED}False{Style.RESET_ALL}"


print("\n\n CHECK TABLE \n\n")

print(f"Button:\t\t{colorize_boolean(BUTTON_check)}")
print(f"Light:\t\t{colorize_boolean(LIGHT_check)}")
print(f"Buzzer:\t\t{colorize_boolean(BUZZER_check)}")
print(f"Joystick:\t{colorize_boolean(JOYSTICK_check)}")
print(f"Distance:\t{colorize_boolean(DISTANCE_check)}")
print(f"QTR:\t\t{colorize_boolean(QTR_check)}")
print(f"Servo:\t\t{colorize_boolean(SERVO_check)}")
print(f"Potantiometer:\t{colorize_boolean(POT_check)}")
print(f"RGB:\t\t{colorize_boolean(RGB_check)}")
print(f"IMU:\t\t{colorize_boolean(IMU_check)}")



input("press Enter")

os.system('cls')

RGBcounter = 0

button_cnt = 0

while True:

    try:
        button = m.get_button(0, modulesID)
    except:
        button = False
    try:
        light = m.get_light(0, modulesID)
    except:
        light = False
    try:
        distance = m.get_distance(0, modulesID)
    except:
        distance = False
    try:
        joystick = m.get_joystick(0, modulesID)
    except:
        joystick = False
    try:
        qtr = m.get_qtr(0, modulesID)
    except:
        qtr = False
    try:
        pot = m.get_potantiometer(0, modulesID)
    except:
        pot = False
    try:
        imu = m.get_imu(0, modulesID)
    except:
        imu = False

    if button == 1:
        button_cnt += 1

    if button_cnt == 5:
        button_cnt = 0

    try:
        qtrToServo = qtr[0]*30 + qtr[1]*60 + qtr[2]*90
    except:
        pass

    try:
        if button == 1:
            m.set_buzzer(0, modulesID, distance*10) # set buzzer by distance
        else:
            m.set_buzzer(0, modulesID, 0) # set buzzer by distance
            buzzer = True
    except:
        buzzer = False

    

    try:
        if button == 1:
            m.set_rgb(0, modulesID, 255, 0, 0)  #set rgb by button
        if button == 2:
            m.set_rgb(0, modulesID, 0, 255, 0)  #set rgb by button
        if button == 3:
            m.set_rgb(0, modulesID, 0, 0, 255)
        if button == 4:
            m.set_rgb(0, modulesID, 255, 255, 255)
        else:
            m.set_rgb(0, modulesID, 0, 0, 0)
        rgb = True
    except:
        rgb = False

    
    try:  
        m.set_servo(0, modulesID, qtrToServo) # set servo by gtr
        servo = True
    except:
        servo = False


    data = [
    ["Button", button],
    ["Light", light],
    ["Buzzer", buzzer],
    ["Joystick", joystick],
    ["Distance", distance],
    ["QTR", qtr],
    ["Servo", servo],
    ["Potantiometer", pot],
    ["RGB", rgb],
    ["IMU", imu]
    ]

    table = tabulate(data, headers=["Component", "Value"], tablefmt="fancy_grid")
    if operatingSystem == 'Windows':
        os.system('cls')    
    else:
        os.system('clear')
    print(table)