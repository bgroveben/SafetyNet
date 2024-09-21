# GPS Rescue

GPS Rescue is a feature commonly found in flight controller software for multirotor drones and other unmanned aerial vehicles (UAVs). Its primary function is to provide an additional layer of safety and redundancy in case of critical in-flight situations where the UAV loses connection with the pilot's remote control or experiences issues with the primary flight controller. GPS Rescue is designed to help the UAV return safely to its takeoff or "home" location.

Here's a more detailed explanation of GPS Rescue:

**1. Safety Mechanism:** GPS Rescue is used as a failsafe mechanism to ensure that the UAV can autonomously navigate and return to a predetermined home location if certain conditions are met, such as losing connection with the remote control, encountering low satellite signal strength, or experiencing an abnormal event.

**2. Home Location:** To use GPS Rescue, the home location must be set at the beginning of the flight when GPS signals are strong and stable. The home location is typically the point where the UAV took off or the initial GPS fix.

**3. Failsafe Activation:** GPS Rescue is typically activated when the UAV loses communication with the remote control, enters a specific flight mode, or when other pre-defined conditions are met.

**4. Flight Phases:** GPS Rescue consists of several flight phases, each with a specific objective:

   - **Initialization:** When GPS Rescue is triggered, the UAV initializes various parameters.
   - **Attain Altitude:** The UAV climbs to a pre-defined altitude to clear obstacles and gain a safe height.
   - **Cross-track:** The UAV aligns itself to a direct path back to the home location.
   - **Landing Approach:** It gets closer to the home location while maintaining the descent altitude.
   - **Landing:** Finally, it initiates the landing procedure at the home location.

**5. Configurable Settings:** GPS Rescue can often be customized and configured according to the pilot's preferences. Parameters such as initial altitude, descent distance, speed, and angles of movement are adjustable.

**6. Safety Checks:** GPS Rescue constantly performs checks for conditions like stall detection (indicating a possible crash), flyaways (unexpected drift away from the home location), GPS signal quality, and more. If any of these checks fail, GPS Rescue might be aborted.

**7. Throttle and Yaw Control:** GPS Rescue also includes control over the throttle (altitude) and yaw (heading) of the UAV. It aims to maintain stability and control throughout the return-to-home process.

**8. Usage in Multicopters:** GPS Rescue is particularly valuable for multicopter drones (quadcopters, hexacopters, etc.) and fixed-wing UAVs. It enhances safety during automated flight modes, autonomous missions, and remote control issues.

**9. Mag (Magnetometer) Usage:** In some implementations, GPS Rescue also takes into account the magnetometer data for heading control. However, if the magnetometer data is unreliable or problematic, it may be temporarily disabled to prevent inaccuracies.

In summary, GPS Rescue is a crucial safety feature in UAV flight controllers that enhances the likelihood of a safe return when critical issues arise. It's an important tool for both recreational drone pilots and professionals who rely on the accuracy and reliability of GPS navigation during their flights. The exact implementation and features can vary between different flight controller software and hardware platforms.

# Cleanflight Implementation

## `gps_rescue`

The code is part of the Cleanflight flight controller software. It's related to GPS Rescue functionality, which is a feature that helps a drone or multirotor aircraft return to its home position or a predefined safe location in case of an emergency or loss of control.

Here's an explanation of how this code works:

1. **Header File (gps_rescue.h):**
   - This is a header file that contains function prototypes and definitions used in the main code file (`gps_rescue.c`).

2. **Main Code File (gps_rescue.c):**
   - The code is organized into several sections, and I'll explain each of them below:

   - **License and Includes:**
     - The code includes the necessary libraries and headers.

   - **Configuration Settings and Types:**
     - The code defines various configuration settings and custom data types to control the behavior of GPS Rescue. These settings include rescue altitude, groundspeed, PID controller gains, etc. Custom data types like `rescueIntent_s` and `rescueSensorData_s` hold the information necessary for GPS Rescue.

   - **Initialization Functions:**
     - The `rescueStart` function initializes the GPS Rescue process.
     - The `rescueStop` function stops GPS Rescue and returns the system to an idle state.

   - **Idle Tasks:**
     - The `idleTasks` function runs tasks that need to be executed regardless of whether GPS Rescue mode is active. It updates information such as maximum altitude, hover throttle, and other flight statistics.

   - **GPS Data Handling:**
     - The `rescueNewGpsData` function is called when new GPS data is received. It updates the home heading information if needed.

   - **Sensor Update:**
     - The `sensorUpdate` function updates various sensor data, including altitude, GPS health, distance to home, and acceleration magnitude.

   - **GPS Rescue State Update:**
     - The `updateGPSRescueState` function is the core of GPS Rescue. It determines the current phase of the rescue operation and computes the necessary control inputs based on the drone's position and altitude relative to the home point.

   - **Sanity Checks:**
     - The `performSanityChecks` function performs checks on the system's health and other criteria to decide if GPS Rescue should continue or if it should be aborted due to potential issues like stalls, GPS signal loss, low satellite count, etc.

   - **Throttle and Yaw Rate Calculation:**
     - The `gpsRescueGetYawRate` function calculates the desired yaw rate for the drone during GPS Rescue.
     - The `gpsRescueGetThrottle` function calculates the desired throttle output based on the rescue throttle settings.

   - **Availability and Disable Functions:**
     - The `gpsRescueIsConfigured` function checks whether GPS Rescue is configured as part of the failsafe procedure.
     - The `gpsRescueIsAvailable` function checks if GPS Rescue is available based on specific criteria.
     - The `gpsRescueIsDisabled` function checks if GPS Rescue is currently disabled.

   - **Magnetometer (Mag) Handling (Optional):**
     - There's code related to optionally disabling the magnetometer (compass) in certain phases of GPS Rescue. This is done to address potential interference issues with the magnetometer.

Please note that this is a high-level overview of the code, and the specific details of each function and its interactions with other parts of the Cleanflight codebase can be quite complex. GPS Rescue is an advanced feature that requires precise control and sensor data to work effectively, and its behavior can be fine-tuned through configuration settings.

## `cms_menu_gps_rescue`

The files  `cms_menu_gps_rescue.c` and `cms_menu_gps_rescue.h` are part of the Cleanflight firmware codebase, which is released under the GNU General Public License. They are related to configuring and managing the GPS rescue feature in Cleanflight. I'll describe each of these files and explain how they relate to each other.

**1. `cms_menu_gps_rescue.c`:**
   - This C source file appears to define and implement the user interface (menu system) for configuring the GPS rescue feature in Cleanflight.
   - It includes several headers for necessary libraries and modules, like `cli/settings.h`, `cms/cms.h`, `flight/gps_rescue.h`, and others.
   - It defines and initializes various configuration parameters for GPS rescue, such as PID values for throttle, yaw, and velocity, altitude settings, ground speed, and more.
   - It provides functions for entering and exiting the GPS rescue PID configuration menu and handles user interaction with this menu.
   - It defines a list of menu entries for configuring GPS rescue PID parameters.

**2. `cms_menu_gps_rescue.h`:**
   - This is a header file, which is typically used for declaring structures, functions, and variables that are defined and implemented in corresponding C files.
   - It declares an external `CMS_Menu` structure named `cmsx_menuGpsRescue`. This structure likely represents the menu for configuring GPS rescue settings.
   - By declaring the menu structure in a header file, other parts of the code can include this header to access and use the `cmsx_menuGpsRescue` menu.

The relationship between these two files is as follows:
- `cms_menu_gps_rescue.c` defines the actual functionality and behavior of the GPS rescue menu system. It implements the menu entries, their functions, and how they interact with the user and the GPS rescue settings.
- `cms_menu_gps_rescue.h` declares the menu structure, which is used to define the menu's properties and contents. It allows other parts of the codebase to access and use this menu by including the header.

In summary, these files work together to create a menu system for configuring GPS rescue settings in the Cleanflight firmware, allowing users to customize various parameters related to GPS-based rescue functionality.

## `position`

The files  `position.c` and `position.h` are part of the Cleanflight firmware codebase, which is released under the GNU General Public License. These files are related to estimating and managing the altitude and position of a multirotor or aircraft. Let's explore how they work and their relationship to the GPS Rescue programs.

**1. `position.c`:**
   - This C source file is responsible for estimating and managing the altitude and position of the aircraft.
   - It includes various necessary headers, such as `platform.h`, `common/maths.h`, `fc/runtime_config.h`, and others.
   - It defines a data structure called `positionConfig_t` for configuring the altitude source (barometer, GPS, or default).
   - It registers this configuration structure with the parameter system (PG_POSITION) and sets a default value.
   - It calculates the estimated altitude and vertical speed (vario) of the aircraft based on data from sensors such as barometers and GPS.
   - The `calculateEstimatedAltitude` function combines altitude data from both barometers and GPS, and the specific data source can be configured through `positionConfig_t`. The algorithm uses a weighted combination of these data sources.
   - If altitude offset information is set, it adjusts the altitude data accordingly.
   - Debug information is also provided to monitor the trust in GPS data, barometer data, and the estimated altitude.
   - Functions like `getEstimatedAltitudeCm` and `getEstimatedVario` allow other parts of the code to access the estimated altitude and vertical speed (vario) values.

**2. `position.h`:**
   - This is a header file that declares the structures and functions defined in `position.c`. It is used to provide external access to these definitions.
   - It declares the `positionConfig_t` structure and its functions, including `isAltitudeOffset`, `calculateEstimatedAltitude`, `getEstimatedAltitudeCm`, and `getEstimatedVario`.
   - By including this header, other parts of the codebase can access and use these functions and the configuration structure.

Regarding their relationship to the GPS Rescue programs:
- These files are not directly related to the GPS Rescue programs but are part of the overall flight control and navigation system.
- The `position` module plays a crucial role in estimating the altitude of the aircraft, which is important for GPS rescue and many other flight control features.
- The GPS rescue programs you mentioned in your previous questions configure various parameters related to GPS-based rescue and PID tuning, but `position.c` focuses on estimating altitude data from sensors.
- The estimated altitude data from `position.c` may be used by other parts of the codebase, including GPS rescue systems, to make decisions and calculations related to altitude.

In summary, `position.c` and `position.h` are responsible for estimating and managing aircraft altitude and position, which can be crucial for various flight control features, including GPS-based rescue systems, but they are not part of the GPS Rescue programs themselves.

# GPS Files Overview

Here is an an overview of the `gps.c` and `gps.h` files, including their variable names, function definitions, dependencies, and their respective purposes.

## `gps.h`

### Purpose
The `gps.h` header file is part of the Cleanflight software project and is primarily used for GPS-related functionality. It defines data structures, constants, enums, and function prototypes for handling GPS data and navigation. It is essential for configuring, parsing, and processing GPS information in the software.

### Variable Names
1. **gpsProvider_e**: An enumeration that defines various GPS providers, such as NMEA, UBLOX, and MSP.
2. **gpsBaudRate_e**: An enumeration for specifying GPS baud rates.
3. **gpsConfig_t**: A structure for storing GPS configuration settings, including provider, SBAS mode, and auto-configuration options.
4. **gpsCoordinateDDDMMmmmm_t**: A structure representing GPS coordinates in a specific format.
5. **gpsLocation_t**: A structure for storing latitude, longitude, and altitude data.
6. **gpsSolutionData_t**: A structure containing GPS solution data, including speed, altitude, and number of satellites.
7. **gpsData_t**: A structure for managing GPS data, including error counters, timeouts, and message states.
8. **gpsUpdateToggle_e**: An enumeration for distinguishing GPS updates.

### Function Definitions
1. `gpsInit()`: Initializes GPS functionality.
2. `gpsUpdate()`: Updates GPS data.
3. `gpsNewFrame(uint8_t c)`: Processes incoming GPS data frames.
4. `gpsIsHealthy()`: Checks for healthy GPS communications.
5. `gpsEnablePassthrough()`: Enables GPS data passthrough.
6. `onGpsNewData()`: Handles new GPS data.
7. `GPS_reset_home_position()`: Resets the home position.
8. `GPS_calc_longitude_scaling()`: Calculates longitude scaling.
9. `GPS_distance_cm_bearing()`: Calculates distance and bearing between two GPS coordinates.

### Dependencies and Other Files
- Dependencies include "axis.h," "time.h," and "pg/pg.h" header files.
- The `gps.c` file interacts with this header file to access GPS-related configurations and structures.

## `gps.c`

### Purpose
The `gps.c` file complements the `gps.h` header file and contains the implementation of the GPS-related functionality within the Cleanflight software project. It handles the initialization, updating, and parsing of GPS data. This code is crucial for acquiring and processing GPS information for navigation and other purposes.

### Variable Names
1. **gpsData**: An instance of the `gpsData_t` structure that keeps track of GPS data and states.
2. **gpsSol**: An instance of the `gpsSolutionData_t` structure for storing GPS solution data.
3. **GPS_home[2]**: An array storing home coordinates (latitude and longitude).
4. **GPS_distanceToHome**: Distance to the home point in meters.
5. **GPS_directionToHome**: Direction to the home point in degrees.
6. **GPS_distanceFlownInCm**: Distance flown since arming in centimeters.
7. **GPS_verticalSpeedInCmS**: Vertical speed in cm/s.
8. **GPS_angle[ANGLE_INDEX_COUNT]**: Angles for GPS correction.
9. **dTnav**: Delta time for navigation computations.
10. **GPS_scaleLonDown**: Used to scale longitude based on latitude.

### Function Definitions
The `gps.c` file contains the implementation of functions declared in `gps.h`. Some of the key functions include:
1. Initialization and configuration of GPS.
2. Parsing and processing incoming GPS data.
3. Calculating distance to home, direction to home, and other navigation-related information.
4. Handling GPS data passthrough and new data updates.
5. Resetting the home position and calculating longitude scaling.

### Dependencies and Other Files
- Dependencies include the `gps.h` header file, "axis.h," "time.h," and "pg/pg.h" header files.
- The `gps.c` file interacts with the `gps.h` header file to access GPS-related configurations, structures, and function prototypes.

## Summary
The `gps.c` and `gps.h` files collectively provide GPS-related functionality within the Cleanflight software project. They define configurations, structures, and functions necessary for acquiring, processing, and using GPS data for navigation and other purposes. The files handle GPS initialization, data processing, and various calculations, making them essential components for GPS functionality in the software.