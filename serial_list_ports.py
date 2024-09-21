import serial.tools.list_ports

# List all available serial ports
available_ports = list(serial.tools.list_ports.comports())

for port, desc, hwid in sorted(available_ports):
    print(f"Port: {port}, Description: {desc}, Hardware ID: {hwid}")

