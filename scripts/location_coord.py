from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from pymavlink import mavutil
import time
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--connect")
args = parser.parse_args()

#connect to the vehicle
vehicle = connect(args.connect, baud=57600, wait_ready=True)

base_location = LocationGlobal()

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

# get location coordinates
def get_location(original_location, dNorth, dEast):

    earth_radius = 6378137.0 

    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)

    if type(original_location)==LocationGlobalRelative:
        target_location = LocationGlobalRelative(newlat, newlon, original_location.alt)
    elif type(original_location)==LocationGlobal:
        target_location = LocationGlobal(newlat, newlon, original_location.alt)
    else:
        raise Exception("Invalid location passed")

    vehicle.simple_goto(target_location)
    
    return None


arm_and_takeoff(3)

print("Take-off complete")

time.sleep(10)

get_location(base_location, 1, 1)
print("reached!!")

print("Landing the vehicle")
vehicle.mode = VehicleMode("LAND")

vehicle.close()