import psutil
import serial
import time

print psutil.cpu_times()

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


while 1:
	time.sleep(1)
	value = psutil.cpu_percent()
	title = run_cmd('mpc current')[15:]
	ser.write("string 0 "+title+ " \r")
	ser.write("value 0 " + str(value) + " \r")
	print "value 0 " + str(value) + "\r"
ser.close()
