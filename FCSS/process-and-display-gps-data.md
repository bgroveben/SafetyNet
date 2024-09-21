# Understanding process_and_display_gps_data.py

`process_and_display_gps_data.py` is a Python script designed to parse NMEA-formatted GPS data and compute various metrics, including distance from previous fixes, speed, altitude, and course. Let's explore how this script works and how it interacts with the updated `pid_main.py` file:

## What the Code Does:

The provided Python script is designed to analyze and display GPS data obtained from NMEA-formatted messages, specifically the `$GPGGA` and `$GPRMC` messages. It calculates and displays various attributes such as latitude, longitude, timestamp, altitude, speed, course, and distances from previous GPS fixes. This script is typically used to process GPS data received from a GPS sensor.

## How It Works:

1. **Conversion Functions (`convert_latitude` and `convert_longitude`):** These functions convert latitude and longitude values from NMEA format (degrees and minutes) to decimal degrees. NMEA format uses degrees and minutes as separate components, so these functions combine them into a single decimal degree value.

2. **`parse_nmea_file` Function:**
   - This function takes the path to a text file containing GPS data in NMEA format as its input.
   - It initializes variables to keep track of the previous latitude and longitude values for both `$GPGGA` and `$GPRMC` messages.
   - It then processes the file line by line using the CSV reader.
   - For each line, it checks whether it's a `$GPGGA` or `$GPRMC` message and extracts relevant information such as timestamp, latitude, longitude, altitude, speed, and course.
   - For both message types, it calculates the distance from the previous fix (if available) using the Haversine formula, which calculates distances on the Earth's surface given two sets of latitude and longitude coordinates.
   - The extracted information is stored in dictionaries, and these dictionaries are appended to the `fixes` list.
   - Finally, the list of dictionaries containing GPS fix information is returned.

3. **Main Section (`if __name__ == "__main__":`):**
   - In the main section of the script, it specifies the path to the GPS data file (`gps_data_file`) that you want to process.
   - It calls the `parse_nmea_file` function to parse the GPS data file and obtain a list of GPS fix dictionaries (`fixes`).
   - It initializes variables (`gpgga_total_distance` and `gprmc_total_distance`) to keep track of the total distances from previous fixes for `$GPGGA` and `$GPRMC` messages.
   - It then iterates through each GPS fix in the `fixes` list and extracts various attributes like speed, altitude, course, and distances from previous fixes.
   - It prints the extracted information, including latitude and longitude, and the cumulative distances from previous fixes for both message types.

## The Fixes and Their Interaction with pid_main.py:

1. **Latitude and Longitude**: The code converts latitude and longitude values from NMEA format to decimal degrees using the `convert_latitude` and `convert_longitude` functions. The converted values are stored in the `ggafix` and `rmcfix` dictionaries. These latitude and longitude values provide the current GPS coordinates and are essential for determining the UAV's position.

2. **Timestamp**: The timestamp is extracted from both GPGGA and GPRMC messages and stored in the `timestamp` field of the respective dictionaries. This timestamp data can be used to synchronize GPS fixes with other data processing in `pid_main.py`.

3. **Altitude**: Altitude is extracted from the GPGGA messages and stored in the `altitude` field of the `ggafix` dictionary. Altitude data can be useful in `pid_main.py` for altitude control and monitoring.

4. **Speed and Course**: Speed and course are extracted from the GPRMC messages and stored in the `speed` and `course` fields of the `rmcfix` dictionary. These values represent the UAV's current speed and course, which are crucial for navigation and control.

5. **Distance from Previous Fix**: The code calculates the distance between consecutive fixes using the Haversine formula, both for GPGGA and GPRMC messages. The distances are added to `gpgga_total_distance` and `gprmc_total_distance`, respectively. These distance measurements can be used in `pid_main.py` for path planning and control adjustments.

6. **Data Display**: The code prints out the extracted data, including speed, altitude, course, latitude, and longitude. It also displays the distances from the previous fixes for both GPGGA and GPRMC messages. This data can be monitored and used for debugging and visualization purposes when running `pid_main.py`.

In summary, `process_and_display_gps_data.py` plays a crucial role in providing updated GPS data to `pid_main.py` for navigation and control. It extracts essential information such as latitude, longitude, altitude, speed, course, and distances from previous fixes, which are used by `pid_main.py` to make real-time decisions and adjustments for steering the UAV along the desired path.

