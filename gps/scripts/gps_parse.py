import serial

port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

def parse_data():
        data = ser.readline()
        data = data.decode('utf-8')
        if data[0:6] == "$GPGLL":
                data_list = data.split(',')
                lat = data_list[1]
                lon = data_list[3]
                if (lat != '' ):
                        lat_deg = lat[0:2]
                        lat_min = lat[2:len(lat)]
                        lon_deg = lon[0:3]
                        lon_min = lon[3:len(lon)]
                        lat_dd = float(lat_deg) + (float(lat_min)/60)
                        lon_dd = float(lon_deg) + (float(lon_min)/60)
                        if( data_list[2] == 'S'):
                                lat_dd = lat_dd*-1
                        if( data_list[4] == 'W'):
                                lon_dd = lon_dd*-1
                        string = str(lat_dd) + ', ' + str(lon_dd) 
                else:
                        string = "No GPS data available"

                return string



