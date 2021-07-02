import socket
import time
import serial
import pynmea2
from datetime import datetime

"""
To use, download the app share GPS and create a USB connection using adb and tcp forward.
Run: adb forward tcp:20175 tcp:50000
"""


# 
# sudo chmod a+rw /dev/ttyUSB0
class LoraEndDevice:
    def __init__(self):

        self.loraSerial = serial.Serial()
        self.loraSerial.port = '/dev/ttyUSB0'
        self.loraSerial.baudrate = 115200
        self.loraSerial.bytesize = 8
        self.loraSerial.parity='N'
        self.loraSerial.stopbits=1
        self.loraSerial.timeout=2
        self.loraSerial.rtscts=False
        self.loraSerial.xonxoff=False

        self.lastAtCmdRx = ''

    def setPortCom(self, newPort):
        self.loraSerial.port = newPort

    def openSerialPort(self):
        self.loraSerial.open()

    def closeSerialPort(self):
        self.loraSerial.close()

    def sendCmdAt(self,cmd):
        if self.loraSerial.is_open:
            self.loraSerial.write(cmd.encode())
        else:
            print('It\'s not possible to communicate with LoRa module!')

    def getAtAnswer(self):
        self.lastAtCmdRx = self.loraSerial.read(100)

    def printLstAnswer(self):
        print(self.lastAtCmdRx.decode('UTF-8'))

    def sendMessage(self, msg):
        msg = '{}\r\n'.format(msg)
        self.sendCmdAt(msg)
        self.getAtAnswer()


endDevice = LoraEndDevice()
endDevice.openSerialPort()

delayBetweenPkt_sec = 3*60 
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
        endDevice.sendMessage('AT')
        endDevice.printLstAnswer()

        id = id+1
        
        time.sleep(delayBetweenPkt_sec)


endDevice.closeSerialPort()