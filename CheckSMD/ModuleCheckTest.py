from smd.red import *

import os
import sys
from serial.tools.list_ports import comports
from platform import system
from colorama import Fore, Style
from tabulate import tabulate
from random import randint


id = 0
module_id = int(input("Please enter the module ID (1-5): "))

#  Serial Port Define
def USB_Port():
    if system() == "Windows":
        ports = list(comports())
        if ports:
            for port, desc, hwid in sorted(ports):
                if 'USB Serial Port' in desc:
                    SMD_Port = port
                    return SMD_Port
        else:
            SMD_Port = None
            return SMD_Port

    elif system() == "Linux":
        ports = list(serial.tools.list_ports.comports())
        if ports:
            for port, desc, hwid in sorted(ports):
                if '/dev/ttyUSB' in port:
                    SMD_Port = port
                    return SMD_Port
        else:
            SMD_port = None
            return SMD_Port

port = USB_Port()
m = Master(port)


m.attach(Red(id))

connected_modules = m.scan_modules(id)

print(connected_modules)

def colorize_str(str, boolean):
    return f"{Fore.GREEN}{str} found!{Style.RESET_ALL}" if boolean else f"{Fore.RED}{str} not found.{Style.RESET_ALL}"

############### Module Test Functions ###############

def button_test(check:bool):
    if check:
        return m.get_button(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"

def buzzer_test(check:bool):
    if check:
        freq = randint(100,4000)
        m.set_buzzer(id, module_id, freq)
        return "Check if buzzer is emitting sound, Hz: {}".format(freq)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"
        
def distance_test(check:bool):
    if check:
        return m.get_distance(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"

def imu_test(check:bool):
    if check:
        return m.get_imu(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"

def joystick_test(check:bool):
    if check:
        return m.get_joystick(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"

def light_test(check:bool):
    if check:
        return m.get_light(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"
    
def pot_test(check:bool):
    if check:
        return m.get_potentiometer(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"


def rgb_test(check:bool):
    if check:
        R = randint(0,255)
        G = randint(0,255)
        B = randint(0,255)

        m.set_rgb(id, module_id, R, G, B)
        time.sleep(0.02)
        return f"{R}, {G}, {B}"
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"


def servo_test(check:bool):
    if check:
        value = randint(0,180)
        m.set_servo(id, module_id, value)
        return f"Check if servo motor has rotated, value: {value}"
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"


def qtr_test(check:bool):
    if check:
        return m.get_qtr(id, module_id)
    else:
        return f"{Fore.RED}Not Connected{Style.RESET_ALL}"


#####################################################

BUTTON_check	= False
BUZZER_check	= False
DISTANCE_check	= False
IMU_check		= False
JOYSTICK_check	= False
LIGHT_check		= False
POT_check	    = False
RGB_check	    = False
SERVO_check		= False
QTR_check	    = False


try:
    if ("Button_" + str(module_id)) in connected_modules:
        BUTTON_check = True

    if ("Buzzer_" + str(module_id)) in connected_modules:
        BUZZER_check = True

    if ("Distance_" + str(module_id)) in connected_modules:
        DISTANCE_check = True

    if ("IMU_" + str(module_id)) in connected_modules:
        IMU_check = True

    if ("Joystick_" + str(module_id)) in connected_modules:
        JOYSTICK_check = True

    if ("Light_" + str(module_id)) in connected_modules:
        LIGHT_check = True

    if ("Pot_" + str(module_id)) in connected_modules:
        POT_check = True

    if ("RGB_" + str(module_id)) in connected_modules:
        RGB_check = True

    if ("Servo_" + str(module_id)) in connected_modules:
        SERVO_check = True

    if ("QTR_" + str(module_id)) in connected_modules:
        QTR_check = True

except:
    print("\nNO MODULES CONNECTED!\n")

module_check_data = [["Button module", colorize_str("Button module", BUTTON_check)],
                     ["Buzzer module", colorize_str("Buzzer module", BUZZER_check)],
                     ["Distance module", colorize_str("Distance module", DISTANCE_check)],
                     ["IMU module", colorize_str("IMU module", IMU_check)],
                     ["Joystick module", colorize_str("Joystick module", JOYSTICK_check)],
                     ["Light module", colorize_str("Light module", LIGHT_check)],
                     ["Potentiometer module", colorize_str("Pot module", POT_check)],
                     ["RGB module", colorize_str("RGB module", RGB_check)],
                     ["Servo module", colorize_str("Servo module", SERVO_check)],
                     ["QTR module", colorize_str("QTR module", QTR_check)]]

module_check_table = tabulate(module_check_data, headers=['Modules', 'States'], tablefmt="rounded_grid")

print(module_check_table)

test_input = str(input("Press enter to start the test, write 'exit' to close the program: "))

m.set_duty_cycle(id, 100)
m.enable_torque(id, 1)

if test_input == "exit":
    sys.exit()

else:
    pass


while True:

    test_result = [ ["Button module", button_test(BUTTON_check)],
                    ["Buzzer module", buzzer_test(BUZZER_check)],
                    ["Distance module", distance_test(DISTANCE_check)],
                    ["IMU module", imu_test(IMU_check)],
                    ["Joystick module", joystick_test(JOYSTICK_check)],
                    ["Light module", light_test(LIGHT_check)],
                    ["Potentiometer module", pot_test(POT_check)],
                    ["RGB module", rgb_test(RGB_check)],
                    ["Servo module", servo_test(SERVO_check)],
                    ["QTR module", qtr_test(QTR_check)]]

    test_table = tabulate(test_result, headers=["Modules", "Results"], tablefmt="rounded_grid")

    if system() == "Windows":
        os.system('cls')
    
    else:
        os.system('clear')

    print(test_table)
    