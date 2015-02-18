import psutil
import serial
import time
from subprocess import *
import os

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(3)
title = run_cmd('mpc current')[:22]
ser.write("mpd 0 "+ title + " \r")

while 1:
	time.sleep(1)
	value = psutil.cpu_percent()
	temp = run_cmd('mpc current')[:22]
	if(temp != title):
		title = temp
		ser.write("mpd 0 "+ title + " \r")
	ser.write("value 0 " + str(value) + " \r")
	ser.write("value 1 " + str(value) + " \r")
	ser.write("value 2 " + str(value) + " \r")
	ser.write("value 3 " + str(value) + " \r")
	ser.write("value 4 " + str(value) + " \r")
	ser.write("value 5 " + str(value) + " \r")
	print "value 0 " + str(value) + "\r"
ser.close()
