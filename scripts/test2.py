from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--connect")
args = parser.parse_args()

#connect to the vehicle
vehicle = connect(args.connect, baud=57600, wait_ready=True)

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

arm_and_takeoff(5)

print("Take-off complete")

time.sleep(15)

print("Landing the vehicle")
vehicle.mode = VehicleMode("LAND")

vehicle.close()