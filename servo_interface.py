from maestro_servo_controller import Controller
# import serial

servo_controller = Controller('/dev/ttyACM0', device=0x0c)
servo_controller.setRange(0, 2000, 8000)  # Set servo 0 range between 2000 and 8000
servo_controller.setTarget(0, 6000)  # Move servo 0 to the center position
if servo_controller.isMoving(0):
    print("Servo 0 is still moving")
servo_controller.close()
