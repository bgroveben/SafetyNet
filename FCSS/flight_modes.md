# Autonomous Flight Control Modes

## Introduction

This document outlines the implementation of essential flight control modes in the `flight_modes.py` script for autonomous fixed-wing flight. The primary modes discussed are Takeoff, Waypoint Navigation, Return to Home (RTH), and Landing. These modes facilitate safe and controlled UAV operation during a simple mission or sortie.

## `flight_modes.py`

### Here's a summary of the functions:

**1. `takeoff`:** Takes off the drone, maintaining altitude at 200 feet. Once the drone reaches the target altitude, it levels off and reduces throttle.

**2. `return_home`:** Navigates the drone back to the home waypoint using the `waypoint_navigation` function and initiates the landing procedure once the drone reaches home.

**3. `landing`:** Guides the drone through a landing procedure. It gradually levels out the plane when the altitude gets down to 5 feet and then reduces throttle.

**4. `waypoint_navigation`:** Guides the drone to a specified latitude and longitude at an altitude of 200 feet using the PID controllers for ailerons and rudder. It returns the final latitude and longitude reached during navigation.

These functions provide the basic control logic for flight modes and navigation. We can further expand on this code to support multiple waypoints, more advanced navigation, and other mission-specific features.

## Takeoff

### Objective

The "Takeoff" mode ensures a controlled ascent from the ground to the desired takeoff altitude.

### Implementation

1. Define a takeoff altitude, either as a constant or from the mission plan.
2. Gradually increase the UAV's throttle to initiate takeoff.
3. Monitor altitude data from GPS.
4. Continue increasing throttle until the desired takeoff altitude is reached.
5. Transition to the "Waypoint Navigation" mode for the next phase of the mission.

## Waypoint Navigation

### Objective

The "Waypoint Navigation" mode allows the UAV to navigate to predefined GPS waypoints as part of the mission.

### Implementation

1. Define a list of GPS waypoints that represent the intended flight path.
2. Implement a waypoint navigation algorithm that guides the UAV to each waypoint.
3. Calculate heading, pitch, and throttle adjustments to maintain the desired flight path.
4. Continuously monitor the UAV's position and progress towards the waypoints.
5. Transition to RTH or Landing mode upon reaching the final waypoint.

## Return to Home (RTH)

### Objective

The "Return to Home" mode ensures the UAV safely returns to its initial takeoff location.

### Implementation

1. Store the initial GPS coordinates (home location) when the UAV takes off.
2. When activating RTH, calculate the UAV's current GPS position.
3. Determine a safe altitude and flight path to return to the home location.
4. Program the UAV to follow this path, adjusting heading, pitch, and throttle as needed.
5. Monitor altitude and trigger the Landing procedure upon nearing home.

## Landing

### Objective

The "Landing" mode guides the UAV to a safe and controlled landing.

### Implementation

1. Initiate the landing procedure by descending the UAV.
2. Maintain control over pitch, heading, and throttle to align with the landing area.
3. Gradually reduce throttle as the UAV approaches the ground to slow descent.
4. Ensure controlled landing by making continuous adjustments to control surfaces and throttle.
5. Disable motors and disarm the system upon a successful landing.

## Safety Considerations

- Maintain safe altitude and attitude during mode transitions.
- Implement obstacle avoidance and safe altitude control during RTH and landing.
- Handle unexpected situations, such as GPS signal loss or communication interruptions.
- Continually monitor system health and sensor data for UAV airworthiness.

These fundamental flight modes provide a foundation for autonomous flight.

