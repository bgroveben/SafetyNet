from pid_servo_controller import PIDController
from maestro_servo_controller import Controller as ServoController
from process_and_display_gps_data import parse_nmea_file, convert_latitude, convert_longitude
from flight_modes import takeoff, waypoint_nav, return_home, landing
import math
import time

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
rudder_channel = 3


def calculate_ailerons_setpoint(current_latitude, current_longitude, target_latitude, target_longitude):
    """
    Calculate the ailerons setpoint based on the difference between current direction and destination.

    Args:
        current_latitude (float): Current latitude of the UAV.
        current_longitude (float): Current longitude of the UAV.
        target_latitude (float): Target latitude.
        target_longitude (float): Target longitude.

    Returns:
        float: Ailerons setpoint for roll control.
    """
    # Calculate the absolute angle of the current direction
    angle_curr = math.atan2(target_longitude - current_longitude, target_latitude - current_latitude)
    if angle_curr < 0:
        angle_curr += 2 * math.pi

    # Calculate the absolute angle of the destination
    angle_dest = math.atan2(target_longitude - current_longitude, target_latitude - current_latitude)
    if angle_dest < 0:
        angle_dest += 2 * math.pi

    # Calculate the relative angle between current direction and destination
    relative_angle = angle_curr - angle_dest
    if relative_angle < -math.pi:
        relative_angle += 2 * math.pi
    elif relative_angle > math.pi:
        relative_angle -= 2 * math.pi

    # Calculate the absolute angle of the difference between current direction and destination
    angle_diff = angle_curr - angle_dest
    if angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    elif angle_diff > math.pi:
        angle_diff -= 2 * math.pi

    # Determine the direction to roll
    if 0 < angle_diff <= math.pi or angle_diff < -math.pi:
        # Roll left
        # Adjust the ailerons servo accordingly
        ailerons_setpoint = 1200.00  # Example value, adjust as needed
    elif -math.pi < angle_diff <= 0 or angle_diff > math.pi:
        # Roll right
        # Adjust the ailerons servo accordingly
        ailerons_setpoint = 1800.00  # Example value, adjust as needed
    else:
        # No roll needed, keep ailerons centered
        ailerons_setpoint = 1500.00  # Example value, adjust as needed

    return ailerons_setpoint


def calculate_elevator_setpoint(current_altitude, target_altitude, lower_threshold, upper_threshold):
    """
    Calculate the elevator setpoint based on the difference between current altitude and target altitude.

    Args:
        current_altitude (float): Current altitude of the UAV in feet.
        target_altitude (float): Target altitude in feet.
        lower_threshold (float): Lower deadband threshold in feet.
        upper_threshold (float): Upper deadband threshold in feet.

    Returns:
        float: Elevator setpoint for altitude control.
    """
    # Check if the current altitude is below the lower deadband threshold
    if current_altitude < lower_threshold:
        # Adjust the elevator to climb (move aircraft up)
        # Increase elevator setpoint
        elevator_setpoint = 1800.00  # Example value, adjust as needed
    # Check if the current altitude is above the upper deadband threshold
    elif current_altitude > upper_threshold:
        # Adjust the elevator to descend (move aircraft down)
        # Decrease elevator setpoint
        elevator_setpoint = 1200.00  # Example value, adjust as needed
    else:
        # Maintain the current altitude (no elevator adjustment needed)
        elevator_setpoint = 1500.00  # Example value, adjust as needed

    return elevator_setpoint


def calculate_throttle_setpoint(current_latitude, current_longitude, target_latitude, target_longitude,
    current_speed, target_speed, current_altitude, target_altitude, course):
    """
    Calculate the throttle setpoint based on GPS data, speed, altitude, and course.
    Args:
        current_latitude (float): Current latitude of the UAV.
        current_longitude (float): Current longitude of the UAV.
        target_latitude (float): Target latitude.
        target_longitude (float): Target longitude.
        current_speed (float): Current speed of the UAV.
        target_speed (float): Target speed.
        current_altitude (float): Current altitude of the UAV in feet.
        target_altitude (float): Target altitude in feet.
        course (float): Current course of the UAV.
    Returns:
        float: Throttle setpoint for speed control.
    """
    # Calculate the absolute angle of the current direction
    angle_curr = math.atan2(target_longitude - current_longitude, target_latitude - current_latitude)
    if angle_curr < 0:
        angle_curr += 2 * math.pi

    # Calculate the absolute angle of the difference between current direction and course
    angle_diff = angle_curr - course
    if angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    elif angle_diff > math.pi:
        angle_diff -= 2 * math.pi

    # Initialize throttle setpoint
    throttle_setpoint = 1500.00  # Default to maintain current speed

    # Throttle control for altitude adjustments (climb and descend)
    if current_altitude < target_altitude:
        # Increase throttle to climb
        throttle_setpoint += 50.00  # Example increment, adjust as needed
    elif current_altitude > target_altitude:
        # Decrease throttle to descend
        throttle_setpoint -= 50.00  # Example decrement, adjust as needed

    # Throttle control for speed adjustments (speed up and slow down)
    if current_speed < target_speed:
        # Increase throttle to speed up
        throttle_setpoint += 50.00  # Example increment, adjust as needed
    elif current_speed > target_speed:
        # Decrease throttle to slow down
        throttle_setpoint -= 50.00  # Example decrement, adjust as needed

    # Ensure the throttle setpoint stays within the valid range (1100 to 2000)
    throttle_setpoint = max(1100.00, min(2000.00, throttle_setpoint))

    return throttle_setpoint


def calculate_rudder_setpoint(current_latitude, current_longitude, target_latitude, target_longitude):
    """
    Calculate the rudder setpoint based on the difference between current direction and destination.

    Args:
        current_latitude (float): Current latitude of the UAV.
        current_longitude (float): Current longitude of the UAV.
        target_latitude (float): Target latitude.
        target_longitude (float): Target longitude.

    Returns:
        float: Rudder setpoint for steering.
    """
    # Calculate the absolute angle of the current direction
    angle_curr = math.atan2(target_longitude - current_longitude, target_latitude - current_latitude)
    if angle_curr < 0:
        angle_curr += 2 * math.pi

    # Calculate the absolute angle of the destination
    angle_dest = math.atan2(target_longitude - current_longitude, target_latitude - current_latitude)
    if angle_dest < 0:
        angle_dest += 2 * math.pi

    # Calculate the relative angle between current direction and destination
    relative_angle = angle_curr - angle_dest
    if relative_angle < -math.pi:
        relative_angle += 2 * math.pi
    elif relative_angle > math.pi:
        relative_angle -= 2 * math.pi

    # Calculate the absolute angle of the difference between current direction and destination
    angle_diff = angle_curr - angle_dest
    if angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    elif angle_diff > math.pi:
        angle_diff -= 2 * math.pi

    # Determine the direction to turn
    if 0 < angle_diff <= math.pi or angle_diff < -math.pi:
        # Turn left
        # Adjust the rudder servo accordingly
        rudder_setpoint = 1200.00  # Example value, adjust as needed
    elif -math.pi < angle_diff <= 0 or angle_diff > math.pi:
        # Turn right
        # Adjust the rudder servo accordingly
        rudder_setpoint = 1800.00  # Example value, adjust as needed
    else:
        # No turn needed, go straight
        rudder_setpoint = 1500.00  # Example value, adjust as needed

    return rudder_setpoint


if __name__ == "__main__":
    # Parse GPS data and get fixes
    gps_data_file = "GPS-DATA--2023-08-18--01-50-01.nmea"
    fixes = parse_nmea_file(gps_data_file)

    # Initialize current positions of control surfaces and other variables
    current_rudder_position = 1500.00  # Initial rudder position (centered)
    current_ailerons_position = 1500.00  # Initial ailerons position (centered)
    current_elevator_position = 1500.00  # Initial elevator position (centered)
    current_latitude = 0.0  # Initialize current latitude
    current_longitude = 0.0  # Initialize current longitude

    # Initialize velocity values for left and right ESCs
    throttle_velocity = 1100.00  # Motor off (minimum velocity)

    # Deadband hysteresis constants
    LowerDeadbandThreshold = 80  # Lower deadband threshold in feet
    UpperDeadbandThreshold = 220  # Upper deadband threshold in feet
    Interval = 10  # Time interval for altitude checks in seconds
    TargetAltitude = 150  # Target altitude in feet (e.g., midway between thresholds)
    TargetSpeed = 10
    TimeElapsed = 0  # Initialize timer

    for i in range(len(fixes)):
        fix = fixes[i]
        if "latitude" in fix and "longitude" in fix:
            if i < len(fixes) - 1:
                target_latitude = fixes[i + 1]["latitude"]
                target_longitude = fixes[i + 1]["longitude"]
                
                # Determine the flight mode and call the corresponding function
                # Here, you can implement your logic to switch between different modes
                if i == 0:
                    takeoff()
                elif i < len(fixes) - 2:
                    waypoint_nav()
                else:
                    return_home()

                # Calculate setpoints for control surfaces
                rudder_setpoint = calculate_rudder_setpoint(
                    current_latitude, current_longitude, target_latitude, target_longitude)
                ailerons_setpoint = calculate_ailerons_setpoint(
                    current_latitude, current_longitude, target_latitude, target_longitude)
                elevator_setpoint = calculate_elevator_setpoint(
                    float(fix["altitude"]), TargetAltitude, LowerDeadbandThreshold, UpperDeadbandThreshold)

                # Calculate PID output for rudder
                rudder_output = rudder_pid.compute(rudder_setpoint, current_rudder_position)

                # Calculate PID output for ailerons
                ailerons_output = ailerons_pid.compute(ailerons_setpoint, current_ailerons_position)

                # Calculate PID output for elevator
                elevator_output = elevator_pid.compute(elevator_setpoint, current_elevator_position)

                # Map PID outputs to servo ranges
                rudder_output_mapped = PIDController.map_to_servo_range(rudder_output, -1, 1, 1200, 1800)
                ailerons_output_mapped = PIDController.map_to_servo_range(ailerons_output, -1, 1, 1200, 1800)
                elevator_output_mapped = PIDController.map_to_servo_range(elevator_output, -1, 1, 1200, 1800)

                # Calculate velocity adjustments for left and right ESCs
                throttle_setpoint = calculate_throttle_setpoint(
                    current_latitude, current_longitude, target_latitude, target_longitude,
                    float(fix["speed"]), TargetSpeed, float(fix["altitude"]), TargetAltitude, float(fix["course"]))


                # Update current positions
                current_rudder_position = rudder_output_mapped
                current_ailerons_position = ailerons_output_mapped
                current_elevator_position = elevator_output_mapped
                current_latitude = fix["latitude"]
                current_longitude = fix["longitude"]

                # Set servo targets for control surfaces and ESCs
                servo_controller.setTarget(rudder_channel, rudder_output_mapped)
                servo_controller.setTarget(ailerons_channel, ailerons_output_mapped)
                servo_controller.setTarget(elevator_channel, elevator_output_mapped)
                servo_controller.setTarget(throttle_channel, throttle_setpoint)

                # Print flight control information
                print(f"Rudder Position: {rudder_output_mapped}")
                print(f"Ailerons Position: {ailerons_output_mapped}")
                print(f"Elevator Position: {elevator_output_mapped}")
                print(f"Altitude: {float(fix['altitude'])} feet")
                print(f"Throttle: {throttle_setpoint}")
                print()

                # Check if it's time to adjust the velocity
                if TimeElapsed >= Interval:
                    # Reset the timer
                    TimeElapsed = 0

                    # Increment or decrement velocity values as needed
                    throttle_velocity += 50.0  # Example increment, adjust as needed


                    # Ensure velocity values stay within the valid range (1100 to 2000)
                    throttle_velocity = max(1100.00, min(2000.00, throttle_velocity))


            # Sleep for a short duration to control loop frequency
            time.sleep(1)

## https://chat.openai.com/c/d8f862e9-1142-46b6-989a-cbf29e15db8b