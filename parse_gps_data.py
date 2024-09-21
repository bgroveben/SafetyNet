import csv

def parse_nmea_file(filename):
  """Parses a text file containing GPS data in NMEA format.
  Args:
    filename: The path to the text file containing the GPS data.
  Returns:
    A list of dictionaries, where each dictionary contains the following keys:
      timestamp: The timestamp of the GPS fix, in the format `YYYY-MM-DD HH:MM:SS.SSS`.
      latitude: The latitude of the GPS fix, in degrees.
      longitude: The longitude of the GPS fix, in degrees.
      altitude: The altitude of the GPS fix, in meters above sea level.
      number_of_satellites_in_view: The number of satellites that were used to calculate the GPS fix.
      hdop: A measure of the accuracy of the horizontal position of the GPS fix.
      vdop: A measure of the accuracy of the vertical position of the GPS fix.

      There are many different message types in NMEA format, each with its own unique purpose. Some of the most common message types include:

        $GPGGA: This message provides the most basic GPS data, including the time, date, latitude, longitude, altitude, number of satellites in view, and horizontal and vertical dilution of precision (HDOP and VDOP).
        $GPGLL: This message provides the same information as $GPGGA, but it also includes the status of the fix (i.e., whether it is a "fix", "2D fix", or "3D fix").
        $GPRMC: This message provides information about the current position, speed, course, and date and time of the last update.
        $GPVTG: This message provides information about the current speed and course over ground (COG).
        $GPGSA: This message provides information about the GPS satellites that were used to calculate the current position.
        $GPGSV: This message provides information about the number of GPS satellites in view, their elevation, azimuth, and signal-to-noise ratio (SNR).

        The first two characters of an NMEA message, such as "$GPGGA", are the message type identifier. The remaining characters in the message provide specific information about the message type. The exact format of each message type is defined by the NMEA 0183 standard.

        Here is a table that summarizes the different message types and their meanings:

        Message Type	Meaning
        $GPGGA	        Global Positioning System Fix Data
        $GPGLL	        Geographic Position, Latitude/Longitude
        $GPRMC	        Recommended Minimum Specific GPS/Transit Data
        $GPVTG	        Course Over Ground and Ground Speed
        $GPGSA	        GPS DOP and Active Satellites
        $GPGSV	        GPS Satellites in View  
  """

  with open(filename, "r") as f:
    reader = csv.reader(f, delimiter=",")

    fixes = []
    for row in reader:
      if row[0] == "$GPGGA":
        fix = {}
        # fix["timestamp"] = row[1] + " " + row[2] + "." + row[3]
        fix["timestamp"] = (row[1])
        fix["latitude"] = (row[2]) + " " + (row[3])
        fix["longitude"] = (row[4]) + " " + (row[5])
        fix["altitude"] = (row[6])
        fix["number_of_satellites_in_view"] = (row[7])
        fix["hdop"] = (row[8])
        fix["vdop"] = (row[9])
        fixes.append(fix)

    return fixes

if __name__ == "__main__":
  # fixes = parse_nmea_file("gps_data.csv")
    fixes = parse_nmea_file("GPS-DATA--2023-08-06--14-24-04.nmea")
  
    for fix in fixes:
        print("Timestamp:", fix["timestamp"])
        print("Latitude:", fix["latitude"])
        print("Longitude:", fix["longitude"])
        print("Altitude:", fix["altitude"])
        print("Number of satellites in view:", fix["number_of_satellites_in_view"])
        print("HDOP:", fix["hdop"])
        print("VDOP:", fix["vdop"])
        print()
        print()
        print("--------------------------------------")
        print("--------------------------------------")
        print()
        print(fix["timestamp"])
        print()


## https://chat.openai.com/c/7ff1281e-8f86-4e9e-aff5-6fcfb89c0c8d