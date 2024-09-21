# common_functions.py
from pid_servo_controller import PIDController
from maestro_servo_controller import Controller as ServoController
from process_and_display_gps_data import parse_nmea_file

# common_functions.py

# Define your PID gains and other parameters
Kp = 1.0
Ki = 0.1
Kd = 0.01

# Create PID controllers and servo controller instances
rudder_pid = PIDController(Kp, Ki, Kd)
left_aileron_pid = PIDController(Kp, Ki, Kd)
right_aileron_pid = PIDController(Kp, Ki, Kd)
servo_controller = ServoController()

# Read and parse GPS data
gps_data_file = "GPS-DATA--2023-08-10--21-27-31.nmea"
fixes = parse_nmea_file(gps_data_file)

# Navigation logic function
def calculate_servo_outputs(current_fix, initial_latitude, initial_longitude):
    # Calculate desired servo positions based on GPS navigation
    # Replace this with your navigation algorithm
    rudder_output = calculate_rudder_output(initial_latitude, initial_longitude, current_fix["latitude"], current_fix["longitude"])
    left_aileron_output = calculate_left_aileron_output(initial_latitude, initial_longitude, current_fix["latitude"], current_fix["longitude"])
    right_aileron_output = calculate_right_aileron_output(initial_latitude, initial_longitude, current_fix["latitude"], current_fix["longitude"])

    # Map PID outputs to servo ranges and set servo targets
    rudder_target = PIDController.map_to_servo_range(rudder_output, -1.0, 1.0, 992, 2000)
    left_aileron_target = PIDController.map_to_servo_range(left_aileron_output, -1.0, 1.0, 992, 2000)
    right_aileron_target = PIDController.map_to_servo_range(right_aileron_output, -1.0, 1.0, 992, 2000)

    # Send target values to servo controller
    servo_controller.setTarget(0, rudder_target)
    servo_controller.setTarget(1, left_aileron_target)
    servo_controller.setTarget(2, right_aileron_target)

    return current_fix["latitude"], current_fix["longitude"]

## https://chat.openai.com/c/7ff1281e-8f86-4e9e-aff5-6fcfb89c0c8d