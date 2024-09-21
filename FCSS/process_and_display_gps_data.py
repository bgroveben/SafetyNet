import csv
import haversine as hs
from haversine import Unit

# Analyze and display GPS data from $GPGGA and $GPRMC messages
# This script was hacked together to keep track of a GPS sensor's timestamp, latitude, longitude, speed, course, and distance from the previous fix.

def convert_latitude(latitude_value):
    """Converts a latitude value from NMEA format to decimal degrees.
    Args:
        latitude_value: The latitude value in NMEA format.
    Returns:
        The latitude value in decimal degrees.
    """
    degrees = int(latitude_value[:2])
    minutes = float(latitude_value[2:])
    converted_latitude = degrees + minutes / 60
    return converted_latitude

def convert_longitude(longitude_value):
    """Converts a longitude value from NMEA format to decimal degrees.
    Args:
        longitude_value: The longitude value in NMEA format.
    Returns:
        The longitude value in decimal degrees.
    """
    degrees = int(longitude_value[:3])
    minutes = float(longitude_value[3:])
    converted_longitude = degrees + minutes / 60
    return converted_longitude

def parse_nmea_file(filename):
    """Parses a text file containing GPS data in NMEA format.
    Args:
        filename: The path to the text file containing the GPS data.
    Returns:
        A list of dictionaries, each containing GPS fix information.
    """
    # Initialize previous coordinates for each fix type
    prev_latitude_gga = None
    prev_longitude_gga = None
    prev_latitude_rmc = None
    prev_longitude_rmc = None
    
    fixes = []
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if row[0] == "$GPGGA":
                ggafix = {}
                ggafix["message"] = row[0]
                ggafix["timestamp"] = row[1]
                ggafix["latitude"] = convert_latitude(row[2])
                ggafix["n_s_indicator"] = row[3]
                ggafix["longitude"] = convert_longitude(row[4])
                ggafix["e_w_indicator"] = row[5]
                ggafix["altitude"] = row[6]
                ggafix["number_of_satellites_in_view"] = row[7]
                ggafix["hdop"] = row[8]
                ggafix["vdop"] = row[9]
                
                if prev_latitude_gga is not None and prev_longitude_gga is not None:
                    location1 = (float(prev_latitude_gga), float(prev_longitude_gga))
                    location2 = (float(ggafix["latitude"]), float(ggafix["longitude"]))
                    distance = hs.haversine(location1, location2, unit=Unit.KILOMETERS)
                    ggafix["distance_from_previous_fix"] = distance
                
                fixes.append(ggafix)
                prev_latitude_gga = ggafix["latitude"]
                prev_longitude_gga = ggafix["longitude"]
            
            elif row[0] == "$GPRMC":
                rmcfix = {}
                rmcfix["message"] = row[0]
                rmcfix["timestamp"] = row[1]
                rmcfix["status"] = row[2]
                rmcfix["latitude"] = convert_latitude(row[3])
                rmcfix["n_s_indicator"] = row[4]
                rmcfix["longitude"] = convert_longitude(row[5])
                rmcfix["e_w_indicator"] = row[6]
                rmcfix["speed"] = row[7]
                rmcfix["course"] = row[8]
                
                if prev_latitude_rmc is not None and prev_longitude_rmc is not None:
                    location1 = (float(prev_latitude_rmc), float(prev_longitude_rmc))
                    location2 = (float(rmcfix["latitude"]), float(rmcfix["longitude"]))
                    distance = hs.haversine(location1, location2, unit=Unit.KILOMETERS)
                    rmcfix["distance_from_previous_fix"] = distance
                
                fixes.append(rmcfix)
                prev_latitude_rmc = rmcfix["latitude"]
                prev_longitude_rmc = rmcfix["longitude"]

    return fixes

if __name__ == "__main__":
    # Parse GPS data and get fixes
    gps_data_file = "GPS-DATA--2023-08-18--01-50-01.nmea"
    fixes = parse_nmea_file(gps_data_file)
    gpgga_total_distance = 0
    gprmc_total_distance = 0

    for fix in fixes:
        if "latitude" in fix and "longitude" in fix:
            target_latitude = fix["latitude"]
            target_longitude = fix["longitude"]

        if "speed" in fix:
            speed = fix["speed"]
            print("Speed:", fix["speed"])

        if "altitude" in fix:
            altitude = fix["altitude"]
            print("Altitude:", fix["altitude"])

        if "course" in fix:
            course = fix["course"]
            print("Course:", fix["course"])

        if "distance_from_previous_fix" in fix and fix['message'] != "$GPRMC":
            gprmc_total_distance += fix["distance_from_previous_fix"]

        if "distance_from_previous_fix" in fix and fix['message'] != "$GPGGA":
            gpgga_total_distance += fix["distance_from_previous_fix"]

        print(f"Latitude: {target_latitude}, Longitude: {target_longitude}")
        print(f"Distance from previous fix (GPRMC): {gprmc_total_distance} kilometers")
        print(f"Distance from previous fix (GPGGA): {gpgga_total_distance} kilometers")
        print()

## https://chat.openai.com/c/d8f862e9-1142-46b6-989a-cbf29e15db8b