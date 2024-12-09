from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException  
import time
import socket
import math
import exceptions
import argparse

def connectMyCopter():
    parser = argparse.ArgumentParser(description="commands")
    parser.add_argument("--connect")
    args = parser.parse_args()

    connection_string = args.connect
    baud_rate = 57600

    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

    return vehicle

def arm():
    while vehicle.is_armable==False:
        print("waiting for vehicle to become armable")
        time.sleep(1)
    print("vehicle is now armable")
    print("") 

    vehicle.armed=True
    while vehicle.armed==False:
        print("waiting for drone to become armed!!")
        time.sleep(1)

    print("vehicle is now armed")
    print("props are spinning")

    return None


vehicle = connectMyCopter()
arm()

print("end of script!!")


