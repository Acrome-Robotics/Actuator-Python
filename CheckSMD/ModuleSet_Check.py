from smd.red import*
from colorama import Fore, Style, init
from tabulate import tabulate
import os
from osModules import*

colorsForRGB = [
    Colors.NO_COLOR,
    Colors.RED,
    Colors.GREEN,
    Colors.BLUE,
    Colors.WHITE,
    Colors.YELLOW,
    Colors.CYAN,
    Colors.MAGENTA,
    Colors.ORANGE,
    Colors.PURPLE,
    Colors.PINK,
    Colors.AMBER,
    Colors.TEAL,
    Colors.INDIGO, 
    Colors.AMBER
    ]

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


port = USB_serial_port()
m = Master(port)
m.attach(Red(0))
ID = 0      #connect to all IDs

modulesList = m.scan_modules(0)
print(modulesList)


try:
    if Index.Button_1 in modulesList:
        BUTTON_check = True
    
    if Index.Light_1 in modulesList:
        LIGHT_check = True

    if Index.Buzzer_1 in modulesList:
        BUZZER_check = True

    if Index.Joystick_1 in modulesList:
        JOYSTICK_check = True   

    if Index.Distance_1 in modulesList:
        DISTANCE_check = True

    if Index.QTR_1 in modulesList:
        QTR_check = True

    if Index.Servo_1 in modulesList:
        SERVO_check = True

    if Index.Pot_1 in modulesList:
        POT_check = True

    if Index.RGB_1 in modulesList:
        RGB_check = True

    if Index.IMU_1 in modulesList:
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


while True:

    try:
        button = m.get_button(0, Index.Button_1)
    except:
        button = False
    try:
        light = m.get_light(0, Index.Light_1)
    except:
        light = False
    try:
        distance = m.get_distance(0, Index.Distance_1)
    except:
        distance = False
    try:
        joystick = m.get_joystick(0, Index.Joystick_1)
    except:
        joystick = False
    try:
        qtr = m.get_qtr(0, Index.QTR_1)
    except:
        qtr = False
    try:
        pot = m.get_potantiometer(0, Index.Pot_1)
    except:
        pot = False
    try:
        imu = m.get_imu(0, Index.IMU_1)
    except:
        imu = False

    if button == 1:
        RGBcounter += 1
    
    if RGBcounter >= 45:
        RGBcounter = 0


    #qtrToServo = qtr[0]*30 + qtr[1]*60 + qtr[2]*90
    
    try:
        buzzer = m.set_buzzer(0, Index.Buzzer_1, (distance < 20)) # set buzzer by distance
    except:
        buzzer = False
    try:
        rgb = m.set_rgb(0, Index.RGB_1, colorsForRGB[RGBcounter//3])  #set rgb by button
    except:
        rgb = False

    try:
        servo = m.set_servo(0, Index.Servo_1, qtrToServo) # set servo by gtr
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

    os.system('cls')
    table = tabulate(data, headers=["Component", "Value"], tablefmt="fancy_grid")
    print(table)