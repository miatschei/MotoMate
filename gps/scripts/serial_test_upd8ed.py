import serial, sys

port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
# file setup
f = open('gps_file2.txt', 'w+')

def parse_data(ser):
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
			msg = str(lat_dd) + ', ' + str(lon_dd)
			return msg


try:
	#temp = None
	loc = None
	while True:
		msg = parse_data(ser)
		if (msg != None):
			#temp = loc
			loc = msg
			f.write(loc)
			f.write('\n')
			print('current location: ' + str(loc) )
		else:
			print('last known location: ' + str(loc) )

except KeyboardInterrupt:
	f.close()
	sys.exit()
