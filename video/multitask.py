from sin_pwm import *
import threading

def driveID():
    pwmSinTaskto80(ID)

def driveID1():
    pwmSinTaskto80(ID1)

def driveID2():
    pwmSinTask(ID2)
 
 
if __name__ =="__main__":
    # creating thread
    t1 = threading.Thread(target=driveID, args=())
    t2 = threading.Thread(target=driveID1, args=())
    t3 = threading.Thread(target=driveID2, args=())
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    t3.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    t3.join()
 
    # both threads completely executed
    print("Done!")