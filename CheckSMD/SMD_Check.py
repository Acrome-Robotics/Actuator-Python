from smd.red import*
import osModules
from colorama import Fore, Style, init


def colorize_boolean(value):
    return f"{Fore.GREEN}True{Style.RESET_ALL}" if value else f"{Fore.RED}False{Style.RESET_ALL}"

#BASICS
COMMUNICATE = False
EEPROM  =   False
REBOOT = False
FACTORY_RESET = False

SET_VALS = False
GET_VALS = False

#MOTOR CONTROL
MOTOR_ROTATION = False
ENCODER_READ = False

TUNE_PID = False

PWM_CONTROL = False
POSITION_CONTROL = False
VELOCITY_CONTROL = False
TORQUE_CONTROL = False

#STARTING
cpr = float(input("CPR = "))
rpm = float(input("RPM = "))


id = 0
cpr = 4741.0
rpm = 100.0


port = osModules.USB_serial_port()
m = Master(port, 115200)

m.attach(Red(0))





try: #COMMUNICATION
    if m.get_driver_info(0) == None:
        COMMUNICATE = False
    else:
        COMMUNICATE = True
    print(m.get_driver_info(0))
except:
    print("COMMUNICATION exception!")

try: #EEPROM, REBOOT
    m.update_driver_id(id, 66)
    id = 66
    m.attach(Red(id))    
    time.sleep(0.5)
    if m.get_driver_info(id) == None:
        COMMUNICATE = False
        REBOOT = False
        EEPROM = False
    else:
        COMMUNICATE = True
        REBOOT = True
        EEPROM = True
    print(m.get_driver_info(id))
except:
    print("EEPROM, REBOOT exception!")

try: # FACTORY RESET
    m.factory_reset(id)
    time.sleep(0.5)
    id = 0
    if m.get_driver_info(id) == None:
        COMMUNICATE = False
        REBOOT = False
        EEPROM = False
        COMMUNICATE = False
        FACTORY_RESET = False
    else:
        COMMUNICATE = True
        REBOOT = True
        EEPROM = True
        COMMUNICATE = True
        FACTORY_RESET = True
    print(m.get_driver_info(id))
except:
    print("FACTORY RESET exception!")

print(f"Communication:\t{colorize_boolean(COMMUNICATE)}")
print(f"EEPROM:\t\t{colorize_boolean(EEPROM)}")
print(f"Reboot:\t\t{colorize_boolean(REBOOT)}")
print(f"Factory Reset:\t{colorize_boolean(FACTORY_RESET)}")
print("\n") 



try: # MOTOR ROTATION, ENCODER READ
    m.update_driver_id(id, 101)
    id = 101
    m.attach(Red(id))
    time.sleep(1)
    m.set_shaft_cpr(id, cpr)
    m.set_shaft_rpm(id, rpm)
    m.set_operation_mode(id, OperationMode.PWM)
    pos = m.get_position(id)[0]
    m.set_duty_cycle(id, 90)
    m.enable_torque(id, True)
    time.sleep(1)

    if m.get_position(id)[0]- pos> (rpm/120)*cpr:
        m.enable_torque(id, False)
        time.sleep(0.2)
        m.set_duty_cycle(id, -90)
        pos = m.get_position(id)[0]
        m.enable_torque(id, True)
        time.sleep(1)
        m.enable_torque(id, False)

        if m.get_position(id)[0] - pos < (rpm/120)*cpr:
            MOTOR_ROTATION = True
            ENCODER_READ = True
    else:
        pass
except:
    print("MOTOR ROTATION, ENCODER exception!")





try:
    m.attach(Red(id))    
    time.sleep(0.5)
    
    m.pid_tuner(id)
    time.sleep(30)
    print("Velocity Control Parameters by PID")
    print(m.get_control_parameters_velocity(id))
    print("Position Control Parameters by PID")
    print(m.get_control_parameters_position(id))
    print(type(m.get_control_parameters_velocity(id)))
    if m.get_shaft_cpr(id)[0]==(cpr):
        if m.get_shaft_rpm(id)[0]==(rpm):
            GET_VALS = True
            SET_VALS = True
    if m.get_control_parameters_position(id)[0] == 1.0:
        TUNE_PID = False
    else:
        TUNE_PID = True
except:
    print("COMMUNICATION exception!")
    

try:
    m.set_operation_mode(id,OperationMode.PWM)
    m.enable_torque(id, 1)
    m.set_duty_cycle(id, 60)
    time.sleep(2)
    pos1 = m.get_position(id)[0]
    time.sleep(2)
    pos2 = m.get_position(id)[0]
    if abs(pos2 - pos1) < 10:
        ENCODER_READ = False
    else:
        ENCODER_READ = True
        PWM_CONTROL = True
    m.enable_torque(id, 0)
    m.set_duty_cycle(id, 0)
except:
    print("COMMUNICATION exception!")
    

print(f"Set Vals:\t{colorize_boolean(SET_VALS)}")
print(f"Get Vals:\t{colorize_boolean(GET_VALS)}")


print(f"Motor Rotation:\t{colorize_boolean(MOTOR_ROTATION)}")
print(f"Encoder Read:\t{colorize_boolean(ENCODER_READ)}")
print(f"Autotune:\t{colorize_boolean(TUNE_PID)}")


print(f"PWM Control:\t{colorize_boolean(PWM_CONTROL)}")
print(f"Position Control:\t{colorize_boolean(POSITION_CONTROL)}")
print(f"Velocity Control:\t{colorize_boolean(VELOCITY_CONTROL)}")
print(f"Torque Control:\t{colorize_boolean(TORQUE_CONTROL)}")



#Finished
while True:
    m.enable_torque(id, 0)
    time.sleep(0.2)
    m.enable_torque(id, 1)
    time.sleep(0.2)



"""
get_latest_fw_version
update_driver_baudrate
get_driver_baudrate
update_master_baudrate


set_variables




factory_reset

ping

reset_encoder
scan_modules
get_driver_info
update_driver_id
enable_torque
pid_tuner
set_operation_mode

set_shaft_cpr
set_shaft_rpm
get_shaft_rpm

set_user_indicator

set_position_limits
get_position_limits

set_torque_limit
get_torque_limit

set_velocity_limit

set_position
get_position
set_velocity
get_velocity
set_torque
get_torque

set_duty_cycle
get_analog_port


set_control_parameters_position
get_control_parameters_position
"""