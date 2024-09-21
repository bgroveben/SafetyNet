import serial
import datetime

# Collect GPS data from external GPS device
def main():

    # Use pyserial to talk to the GPS via USB
    ser = serial.Serial("/dev/cu.usbmodem14101", baudrate=9600)
    ser.flushInput()
    ser.flushOutput()

    nmea_messages = 0
    nmea_data = b""
    # Why a bytes object? It works for now.

    print("Collecting GPS data...")

    # Use a try/except block in case the serial port is not available.
    try:
        for _ in range(600):
            nmea_messages += 1
            nmea_sentence = ser.readline()
            nmea_data += nmea_sentence
            if nmea_messages % 50 == 0:
                print(f"nmea_messages: {nmea_messages}")
        
        if nmea_messages == 600:
                # save to file after 600 sentences added
                filename = datetime.datetime.now().strftime("GPS-DATA--%Y-%m-%d--%H-%M-%S.nmea")
                with open(filename, "ab") as f:
                    f.write(nmea_data)
                    nmea_data = b""
                print("GPS data collected.")

    except serial.SerialException as e:
        print(e)

if __name__ == "__main__":
    main()

## https://chat.openai.com/c/d8f862e9-1142-46b6-989a-cbf29e15db8b