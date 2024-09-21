import math 


class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, setpoint, current_value):
        error = setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error

        return output

    @staticmethod
    def map_to_servo_range(value, min_val, max_val, min_range, max_range):
        return int(((value - min_val) / (max_val - min_val)) * (max_range - min_range) + min_range)

"""
# Assuming you have a list of GPS coordinates [(latitude, longitude)] over time
gps_coordinates = [
    (latitude1, longitude1),
    (latitude2, longitude2),
    (latitude3, longitude3),
    # ...
]
"""

# Constants for the PID controller
Kp = 1.0  # Proportional gain
Ki = 0.1  # Integral gain
Kd = 0.2  # Derivative gain

# Initialize the PID controller
pid_controller = PIDController(Kp, Ki, Kd)
"""
# Set the initial reference coordinates
reference_latitude, reference_longitude = gps_coordinates[0]

for latitude, longitude in gps_coordinates:
    # Calculate heading using trigonometric functions
    delta_longitude = longitude - reference_longitude
    heading_rad = math.atan2(delta_longitude, math.radians(latitude - reference_latitude))
    heading_deg = math.degrees(heading_rad)
    
    # Calculate PID output
    servo_output = pid_controller.compute(reference_heading, heading_deg)
    
    # Apply the servo output to steer the UAV
    # servo.set_position(servo_output)
    print(f"Latitude: {latitude}, Longitude: {longitude} | Heading: {heading_deg}° | Servo Output: {servo_output}")
"""

## https://chat.openai.com/c/d8f862e9-1142-46b6-989a-cbf29e15db8b