import psutil
import serial
import time

print psutil.cpu_times()

ser = serial.Serial('/dev/ttyACM0', 19200, timeout=1)

while 1:
	time.sleep(5)
	value = psutil.cpu_percent()
	ser.write("value 0" + str(value))
	print "value 0 " + str(value)
ser.close()
