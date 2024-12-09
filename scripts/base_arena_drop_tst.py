from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--connect")
args = parser.parse_args()

#connect to the vehicle
vehicle = connect(args.connect, baud=57600, wait_ready=True)

# coordinates
base_coord = LocationGlobalRelative()
arena_coord = LocationGlobalRelative()
drop_coord = LocationGlobalRelative()


# arm and take off the drone
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

# first go to arena
def goto_arena(arena_loc):

    vehicle.simple_goto(arena_loc)

    return None

# descend slowly
def descend(vx, vy, vz, duration):

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0b0000111111000111,
        0,0,0,
        vx, vy, vz,
        0,0,0,
        0,0)

    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
    
    return None

# ascend from arena and go to drop zone
def ascend_goto(drop_loc, vx, vy, vz, duration):

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0b0000111111000111,
        0,0,0,
        vx, vy, -vz,
        0,0,0,
        0,0)

    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

    vehicle.simple_goto(drop_loc)
    
    return None

# takes of to the specified height
arm_and_takeoff(4)
print("Take-off complete")
time.sleep(10)

# from there moves to arena
goto_arena(arena_coord)

# in arena descends and picks-up the package
descend(0, 0, 1, )

# from there ascends and moves to the drop zone
ascend_goto(drop_coord, 0, 0, 1, )

# descends and drop the package
descend(0, 0, 1, )

# ascends and moves to base location
ascend_goto(base_coord, 0, 0, 1, )

#land the vehicle and closes
print("Landing")
vehicle.mode = VehicleMode("LAND")
vehicle.close()



