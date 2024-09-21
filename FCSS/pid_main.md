# UAV Navigation Script - `pid_main.py`

`pid_main.py` is designed to control the navigation of a UAV (Unmanned Aerial Vehicle) based on GPS coordinates and altitude information. It adjusts the rudder, elevator, and aileron controls, as well as the Electronic Speed Controllers (ESCs) for the UAV's motors. Below, we'll explain the functionality and key components of the script.

## Table of Contents
- [Introduction](#introduction)
- [Functions](#functions)
- [Main Function](#main-function)
- [Initialization](#initialization)
- [GPS Data Processing](#gps-data-processing)
- [Control Loop](#control-loop)

## Introduction

The script relies on several libraries for its functionality:
- `pid_servo_controller`: Provides PID controller capabilities for managing control loops.
- `maestro_servo_controller`: Offers a controller for servos and ESCs.
- `process_and_display_gps_data`: A custom module for processing GPS data.
- `math`: The built-in Python math library for mathematical operations.
- `time`: The built-in Python time library for adding delays in the script.

## Functions

The script defines three functions to calculate control setpoints for different aspects of UAV control:
1. `calculate_rudder_setpoint`: Calculates the rudder control setpoint for yaw control based on the difference between the current direction and the target GPS coordinates.
2. `calculate_elevator_setpoint`: Computes the elevator control setpoint for pitch control.
3. `calculate_ailerons_setpoint`: Determines the ailerons control setpoint for roll control.

Each of these functions calculates control setpoints based on the difference in angles between the current UAV position and the target coordinates.

## Main Function

The main part of the script is enclosed in an `if __name__ == "__main__":` block, ensuring that it only runs when the script is executed directly, not when imported as a module.

## Initialization

The script initializes PID controllers and a ServoController instance:
- PID gains (`Kp`, `Ki`, and `Kd`) are defined for rudder, elevator, and aileron control loops.
- Three PID controllers (`rudder_pid`, `elevator_pid`, and `ailerons_pid`) are created with these gains.
- An instance of the `ServoController` class is created. Initialization specifics depend on the actual implementation of this class.

## GPS Data Processing

- The script parses GPS data from a file (specified by `gps_data_file`).
- The assumption is that the file contains latitude, longitude, and altitude information from NMEA messages.

## Control Loop

The core of the script is the control loop, which iterates through the parsed GPS data:
- For each GPS fix, the script calculates control setpoints for rudder, elevator, and aileron controls based on the difference between the current and target GPS coordinates.
- PID controllers compute control outputs based on the setpoints.
- The control outputs are mapped to servo and ESC ranges.
- Servo and ESC channels are set to the mapped control outputs using the `servo_controller.setTarget` method.
- A delay of 1 second is added between iterations.
