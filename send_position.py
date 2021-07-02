import socket
import serial
import pynmea2
from datetime import datetime

"""
To use, download the app share GPS and create a USB connection using adb and tcp forward.
Run: adb forward tcp:20175 tcp:50000
"""

ser = serial.Serial('/dev/pts/2') #LoRa serial port


HOST = 'localhost'  # The server's hostname or IP address
PORT = 20175        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    id=0
    while 1:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        data = s.recv(1024).decode("utf-8")
        position = data.splitlines(0)[0]
        latitude = pynmea2.parse(position).lat
        longitude = pynmea2.parse(position).lon
        altitude = pynmea2.parse(position).altitude

        data_to_send = '[{}] Id.:{}, Lat.: {}, Lon.: {}, Alt.:{}'.format(time, id, latitude, longitude, altitude)

        print(data_to_send)
        ser.write(str.encode(data_to_send+'\n\r'))
        id = id+1
        
