from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException  
import time
import socket
import math
import exceptions
import argparse


### connecting to the vehicle
def connectMyCopter():
    parser = argparse.ArgumentParser(description="commands")
    parser.add_argument("--connect")
    args = parser.parse_args()

    connection_string = args.connect
    baud_rate = 57600

    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

    return vehicle

# arm and take off the vehicle
def arm_and_takeoff(target_altitude):

    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for vehicle to be armed")
        time.sleep(1)

    print("Take-off")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print("Altitude : ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# simple go to a location
def 
goto(target_location):

    print("location received")
    print("Reaching destination!!")
    print("")

    vehicle.simple_goto(target_location)
    return None

# descending 
def descend(vx, vy, vz, duration):

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0,0,0,
        vx, vy, vz,
        0,0,0,
        0,0)

    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


vehicle = connectMyCopter()

arm_and_takeoff(3)
print("take of complete")

time.sleep(3)

goto(())

descend(0, 0, 3)

print("completed")

vehicle.close()







    