# flight_modes.py
import haversine as hs
from haversine import Unit
from pid_servo_controller import PIDController
from maestro_servo_controller import Controller as ServoController
from process_and_display_gps_data import parse_nmea_file
# import math
# import time

# Specify your GPS data file
gps_data_file = "GPS-DATA--2023-08-18--01-50-01.nmea"
# Call the parse_nmea_file function to obtain GPS fixes
fixes = parse_nmea_file(gps_data_file)

# Constants for PID gains
Kp = 1.0
Ki = 0.1
Kd = 0.01

# Create PID controllers for rudder and ailerons
rudder_pid = PIDController(Kp, Ki, Kd)
elevator_pid = PIDController(Kp, Ki, Kd)
ailerons_pid = PIDController(Kp, Ki, Kd)
throttle_pid = PIDController(Kp, Ki, Kd)

# Create a ServoController instance
servo_controller = ServoController()

# Define servo channels (Mode 2 configuration)
ailerons_channel = 0
elevator_channel = 1
throttle_channel = 2
rudder_channel   = 3

def takeoff(ailerons_pid, elevator_pid, servo_controller, fixes):
    # Set initial positions for ailerons and rudder (midpoint)
    ailerons_setpoint = 1500.00
    rudder_setpoint = 1500.00

    # Set initial positions for ESCs and elevator (full throttle and climb)
    elevator_setpoint = 1800.00
    throttle_setpoint = 1800.00

    # You'll need to update current positions accordingly if needed
    current_rudder_position = 1500.00
    current_ailerons_position = 1500.00

    # Find the first altitude reading in the GPS data
    current_altitude = None
    for i in range(len(fixes)):
        fix = fixes[i]
        for fix in fixes:
            if "altitude" in fix:
                #if i < len(fixes) - 1:
                current_altitude = float(fix["altitude"])
                break

    # While the current altitude is less than 200 feet
    while current_altitude is not None and current_altitude < 200:
        # Calculate PID output for ailerons (assuming you want to maintain level)
        ailerons_output = ailerons_pid.compute(ailerons_setpoint, current_ailerons_position)

        # Calculate PID output for rudder (assuming you want to maintain level)
        rudder_output = rudder_pid.compute(rudder_setpoint, current_rudder_position)

        # Map PID outputs to servo ranges
        ailerons_output_mapped = PIDController.map_to_servo_range(ailerons_output, -1, 1, 1200, 1800)
        rudder_output_mapped = PIDController.map_to_servo_range(rudder_output, -1, 1, 1200, 1800)

        # Set servo targets for ailerons, rudder, ESCs, and elevator
        servo_controller.setTarget(ailerons_channel, ailerons_output_mapped)
        servo_controller.setTarget(rudder_channel, rudder_output_mapped)
        servo_controller.setTarget(throttle_channel, throttle_setpoint)
        servo_controller.setTarget(elevator_channel, elevator_setpoint)

        # Update current positions if needed
        current_ailerons_position = ailerons_output_mapped
        current_rudder_position = rudder_output_mapped

        # Find the next altitude reading in the GPS data
        for fix in fixes:
            if "altitude" in fix and float(fix["altitude"]) > current_altitude:
                current_altitude = float(fix["altitude"])
                break

    # Once the altitude has reached 200 feet, set ESCs and elevator back to midpoint
    throttle_setpoint = 1500.00
    elevator_setpoint = 1500.00
    servo_controller.setTarget(throttle_channel, throttle_setpoint)
    servo_controller.setTarget(elevator_channel, elevator_setpoint)

    # Update current positions if needed
    # current_elevator_position = elevator_setpoint

def return_home(ailerons_pid, rudder_pid, servo_controller, fixes, home_latitude, home_longitude):
    # Navigate to the home waypoint
    final_latitude, final_longitude = waypoint_navigation(ailerons_pid, rudder_pid, servo_controller, fixes, home_latitude, home_longitude)

    # Once the drone reaches home, initiate the landing procedure
    landing(ailerons_pid, elevator_pid, servo_controller, fixes)



def landing(ailerons_pid, elevator_pid, servo_controller, fixes):
    # Assuming you've determined the landing point or altitude
    landing_altitude = 5  # Set this to your desired landing altitude in feet

    # Set initial positions for ailerons and rudder (midpoint)
    ailerons_setpoint = 1500.00
    rudder_setpoint = 1500.00

    # Set initial positions for ESCs (throttle is reduced for landing)
    throttle_setpoint = 1300.00  # Adjust as needed

    # Set initial position for elevator (start descent)
    elevator_setpoint = 1200.00  # Begin descent

    # You'll need to update current positions accordingly if needed
    current_rudder_position = 1500.00
    current_ailerons_position = 1500.00
    current_elevator_position = 1200.00  # Start with elevator set to begin descent

    # Find the first altitude reading in the GPS data
    current_altitude = None
    for fix in fixes:
        if "altitude" in fix:
            current_altitude = float(fix["altitude"])
            break

    # Create a flag to indicate when to cut throttle
    cut_throttle_flag = False

    # Initialize timestamps for throttle reduction
    cut_throttle_timestamp = None

    # While the current altitude is above the landing altitude
    while current_altitude is not None and current_altitude > landing_altitude:
        # Calculate PID output for ailerons (maintain level)
        ailerons_output = ailerons_pid.compute(ailerons_setpoint, current_ailerons_position)

        # Calculate PID output for rudder (maintain level)
        rudder_output = rudder_pid.compute(rudder_setpoint, current_rudder_position)

        # Calculate elevator setpoint based on altitude
        if current_altitude > 100:
            elevator_setpoint = 1200.00
        elif current_altitude > 50:
            elevator_setpoint = 1300.00
        elif current_altitude > 5:
            elevator_setpoint = 1400.00
        else:
            elevator_setpoint = 1550.00

        # Map PID outputs to servo ranges
        ailerons_output_mapped = PIDController.map_to_servo_range(ailerons_output, -1, 1, 1200, 1800)
        rudder_output_mapped = PIDController.map_to_servo_range(rudder_output, -1, 1, 1200, 1800)
        elevator_output_mapped = PIDController.map_to_servo_range(elevator_setpoint, 1200, 1550, 1550, 1500)

        # Set servo targets for ailerons, rudder, elevator, and reduced throttle for landing
        servo_controller.setTarget(ailerons_channel, ailerons_output_mapped)
        servo_controller.setTarget(rudder_channel, rudder_output_mapped)
        servo_controller.setTarget(throttle_channel, throttle_setpoint)
        servo_controller.setTarget(elevator_channel, elevator_output_mapped)

        # Update current positions if needed
        current_ailerons_position = ailerons_output_mapped
        current_rudder_position = rudder_output_mapped
        current_elevator_position = elevator_output_mapped

        # Find the next altitude reading in the GPS data
        for fix in fixes:
            if "altitude" in fix and float(fix["altitude"]) > current_altitude:
                current_altitude = float(fix["altitude"])
                break

        # Check if altitude is close to 5 feet to gradually level out for a smooth landing
        if current_altitude <= 5 and not cut_throttle_flag:
            cut_throttle_timestamp = None  # Reset the timestamp
            cut_throttle_flag = True

        # Once the altitude is close to 0 feet, initiate throttle reduction
        if current_altitude <= 0:
            # Gradually level the plane
            if cut_throttle_timestamp is None:
                # Store the timestamp when altitude reaches 0
                for fix in fixes:
                    if "altitude" in fix and float(fix["altitude"]) <= 0:
                        cut_throttle_timestamp = fix["timestamp"]
                        break
            else:
                # Cut throttle to 1200 for 5 seconds (adjust as needed)
                if "altitude" in fix and fix["timestamp"] >= cut_throttle_timestamp:
                    throttle_setpoint = 1200.00
                else:
                    # Reduce throttle further to 1100 after 5 seconds
                    throttle_setpoint = 1100.00

            servo_controller.setTarget(throttle_channel, throttle_setpoint)

    # Once the drone has descended to the landing altitude and completed the landing procedure
    # Perform any final landing procedures here (e.g., shutting down motors)


def waypoint_navigation(ailerons_pid, rudder_pid, servo_controller, fixes, home_latitude, home_longitude):
    # Altitude for waypoint navigation
    waypoint_altitude = 200.0  # 200 feet

    # Initialize positions and setpoints
    ailerons_setpoint = 1500.00
    rudder_setpoint = 1500.00
    elevator_setpoint = 1500.00

    # Initialize current latitude and longitude with the first coordinates from the GPS data
    if fixes:
        current_latitude = fixes[0]["latitude"]
        current_longitude = fixes[0]["longitude"]
    else:
        current_latitude = None
        current_longitude = None

    # Initialize target latitude and longitude with the last coordinates from the GPS data
    if fixes:
        target_latitude = fixes[-1]["latitude"]
        target_longitude = fixes[-1]["longitude"]
    else:
        target_latitude = home_latitude
        target_longitude = home_longitude

    # Set initial throttle for altitude
    throttle_setpoint = 1800.00

    # Initialize current altitude
    current_altitude = None

    # Find the first altitude reading in the GPS data
    for fix in fixes:
        if "altitude" in fix:
            current_altitude = float(fix["altitude"])
            break

    # Loop until the drone reaches the waypoint or receives further instructions
    while True:
        # Calculate PID output for ailerons and rudder to maintain level flight
        ailerons_output = ailerons_pid.compute(ailerons_setpoint, ailerons_setpoint)  # Maintain level
        rudder_output = rudder_pid.compute(rudder_setpoint, rudder_setpoint)  # Maintain level

        # Map PID outputs to servo ranges
        ailerons_output_mapped = PIDController.map_to_servo_range(ailerons_output, -1, 1, 1200, 1800)
        rudder_output_mapped = PIDController.map_to_servo_range(rudder_output, -1, 1, 1200, 1800)

        # Set servo targets for ailerons, rudder, elevator, and throttle
        servo_controller.setTarget(ailerons_channel, ailerons_output_mapped)
        servo_controller.setTarget(rudder_channel, rudder_output_mapped)
        servo_controller.setTarget(elevator_channel, elevator_setpoint)
        servo_controller.setTarget(throttle_channel, throttle_setpoint)

        # Check if the drone has reached the waypoint
        if current_latitude is not None and current_longitude is not None:
            #distance_to_target = calculate_distance(current_latitude, current_longitude, target_latitude, target_longitude)
            distance_to_target = hs.haversine(current_latitude, current_longitude, target_latitude, target_longitude, unit=Unit.KILOMETERS)

            # If the drone is within an acceptable range of the waypoint, break the loop
            if distance_to_target < 0.01:  # Adjust this threshold as needed
                break

        # Check for further instructions to continue to the next waypoint or return home
        # For simplicity, you can use a flag or some external trigger

    return current_latitude, current_longitude
