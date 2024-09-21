# from common_functions import fixes, calculate_servo_outputs
from common_functions import fixes, calculate_servo_outputs, Kp, Ki, Kd

# Set initial waypoints (latitude and longitude)
initial_latitude = fixes[0]["latitude"]
initial_longitude = fixes[0]["longitude"]

# Example navigation loop using GPS data
for i in range(1, len(fixes)):
    current_fix = fixes[i]

    initial_latitude, initial_longitude = calculate_servo_outputs(current_fix, initial_latitude, initial_longitude)


## https://chat.openai.com/c/7ff1281e-8f86-4e9e-aff5-6fcfb89c0c8d