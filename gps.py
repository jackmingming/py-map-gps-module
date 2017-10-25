import serial
import json

class gps():

    def __init__(self, serial_port, gps_speed):
        self.serial_port = serial_port
        self.serial_speed = gps_speed

        self.GPS_DATA_FORMATED = {
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

        self.connect_to_gps()

    def connect_to_gps(self):
        try:
            self.serial = serial.Serial(self.serial_port, self.serial_speed, timeout = 1)
            self.serial.flushInput()
            self.serial.flushOutput()
        except Exception as e:
            pass

    def init_data(self):
        if self.serial.isOpen():
            self.GPS_Data = self.serial.readline()
            if self.GPS_Data:
                yield self.parse_Response(self.GPS_Data)

    def parse_Response(self, GPS_Line):
        
        gpsChars = GPS_Line
        chkVal = 1

        if "*" not in gpsChars:
            return False

        gpsStr, chkSum = gpsChars.split('*')
        gpsComponents = gpsStr.split(',')
        gpsStart = gpsComponents[0]

        if (gpsStart == "$GNGGA"):
            chkVal = 0

        for ch in gpsStr[1:]:
            chkVal ^= ord(ch)

        if (chkVal == int(chkSum, 16)):
            for i, k in enumerate(
                ['strType', 'fixTime', 'lat', 'latDir', 
                'lon', 'lonDir', 'fixQual', 'numSat', 
                'horDil', 'alt', 'altUnit', 'galt', 
                'galtUnit','DPGS_updt', 'DPGS_ID']): 

                self.GPS_DATA_FORMATED[k] = gpsComponents[i]

                if k == "lat":
                    gps_coordinator_lat = self.parse_Lat(gpsComponents[i])
                    self.GPS_DATA_FORMATED[k] = gps_coordinator_lat

                if k == "lon":
                    gps_coordinator_lat = self.parse_Lon(gpsComponents[i])
                    self.GPS_DATA_FORMATED[k] = gps_coordinator_lat
                        
            # print 'Original GPS Data: ' + gpsChars
            # print 'raw: ', json.dumps(self.GPS_DATA_FORMATED, indent = 2)

            return  self.GPS_DATA_FORMATED

    def parse_Lat(self, lat):

        degress = int(lat[0:2])
        minutes = float(lat[2:]) / 60
        gps_coordinator_lat = float(degress + minutes)

        return gps_coordinator_lat

    def parse_Lon(self, lon):

        degress = int(lon[0:3])
        minutes = float(lon[3:]) / 60
        gps_coordinator_lon = float(degress + minutes)

        return gps_coordinator_lon    
        

