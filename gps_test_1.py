import serial
import time
import json
serial_speed = 9600
serial_port = '/dev/tty.wchusbserial'
ser = serial.Serial(serial_port, serial_speed, timeout = 1)

GPSDAT = {
    'strType': None,
    'fixTime': None,
    'lat': None,
    'latDir': None,
    'lon': None,
    'lonDir': None,
    'fixQual': None,
    'numSat': None,
    'horDil': None,
    'alt': None,
    'altUnit': None,
    'galt': None,
    'galtUnit': None,
    'DPGS_updt': None,
    'DPGS_ID': None
}

def parseResponse(gpsLine):
    global lastLocation
    gpsChars = gpsLine
    if "*" not in gpsChars:
        return False

    gpsStr, chkSum = gpsChars.split('*')    
    gpsComponents = gpsStr.split(',')
    gpsStart = gpsComponents[0]
    if (gpsStart == "$GNGGA"):
        chkVal = 0
        for ch in gpsStr[1:]: # Remove the $
            chkVal ^= ord(ch)
        if (chkVal == int(chkSum, 16)):
            for i, k in enumerate(
                ['strType', 'fixTime', 
                'lat', 'latDir', 'lon', 'lonDir',
                'fixQual', 'numSat', 'horDil', 
                'alt', 'altUnit', 'galt', 'galtUnit',
                'DPGS_updt', 'DPGS_ID']):
                GPSDAT[k] = gpsComponents[i]
            print gpsChars
            print json.dumps(GPSDAT, indent=2)

while True:
     data = ser.readline()
     if data:
        # parseResponse(data)
        print data