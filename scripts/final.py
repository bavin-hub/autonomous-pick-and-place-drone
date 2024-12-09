import numpy
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time, math
import argparse

##### connect to vehicle #####
parser = argparse.ArgumentParser()
parser.add_argument("--connect")
args = parser.parse_args()
vehicle = connect(args.connect, baud=57600, wait_ready=True)
################
arena_lat = 12.9893572
arena_lon = 80.2374021
drop_lat = 12.9894363
drop_lon = 80.2373875
alt = 2
arena = LocationGlobalRelative(arena_lat, arena_lon, alt)
drop = LocationGlobalRelative(drop_lat, drop_lon, alt)
### arm and takeoff
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
###########

##### velocity commands
def velocity(vx, vy, vz, duration):

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
#########

###### simple goto 
def simple(target_location):

    print("location received")
    print("")
    vehicle.airspeed = 3
    vehicle.groundspeed = 5
    vehicle.simple_goto(target_location)
################

######## yaw 
def yaw(heading, relative=False):

    if relative:
        is_relative=1
    else:
        is_realtive=0

    msg = vehicle.message_factory.command_long_encode(
        0,0,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        heading,
        0,
        1,
        is_relative,
        0,0,0)

    vehicle.send_mavlink(msg)
###############

####### get distance meters
def get_dist_met(loc_a, loc_b):
    lat = loc_b.lat - loc_a.lat
    lon = loc_b.lon - loc_a.lon
    return math.sqrt((lat*lat) + (lon*lon)) * 1.113195e5
#################

arm_and_takeoff(alt)
print("Take of complete!!")
time.sleep(8)

simple(arena)
time.sleep(8)
("reached arena")

velocity(0,0,0.386, 5)
time.sleep(7)
velocity(0,0,-0.386, 5)
time.sleep(3)

simple(drop)
velocity(0,0,0.386, 5)
time.sleep(7)
velocity(0,0,-0.386, 5)
time.sleep(3)

vehicle.mode = VehicleMode("RTL")
time.sleep(4)

vehicle.mode = VehicleMode("LAND")
vehicle.close()