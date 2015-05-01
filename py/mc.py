#!/usr/bin/python
#
#music and control daemon

import os,sys,time,serial,json,psutil,threading,argparse,aor
import RPi.GPIO as GPIO
import aor.mpc as MPC
from bson import BSON, json_util
from subprocess import *
from datetime import datetime
from termcolor import colored


parser = argparse.ArgumentParser(description="AOR 2015")
parser.add_argument("-n", "--nolog", help="no log, use stdio", default=False, action="store_true")
args = parser.parse_args()

if not args.nolog:
	aor.stdio_logger.use_logging_handler(filename="/var/log/aor/mc.log",level="debug")

config = json.loads(open('/home/debauer/AOR2015/configs/aor_service.json').read())

playlist_lines = config['music']['playlist_lines']
hostname = config['hostname']
keyvalues = config['keyvalues']
w1 = config['w1']
circle_sleep = int(config['circle_sleep'])
telegram_sleep = float(config['telegram_sleep'])

keyvalue 	= aor.keyvalue.KeyValue(mongo=config['store']['mongo'],redis=config['store']['redis'])
log 		= aor.logger.Logger(rrd=config['store']['rrd'],influx=config['store']['influx'],influx_config=config['influx'])

use_serial = True
lcd_seite = 0

GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False) 

ENCODER_1 		= 33
ENCODER_2 		= 35
BUTTON_ENCODER  = 37
BUTTON_NEXT		= 40
BUTTON_PREV		= 38
BUTTON_UP		= 22
BUTTON_DOWN		= 18

GPIO.setup(ENCODER_1, 		GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ENCODER_2, 		GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_ENCODER, 	GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_NEXT, 	GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(BUTTON_PREV,		GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(BUTTON_UP, 		GPIO.IN, pull_up_down = GPIO.PUD_UP) 
GPIO.setup(BUTTON_DOWN, 	GPIO.IN, pull_up_down = GPIO.PUD_UP) 

GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=MPC.next, bouncetime=300)
GPIO.add_event_detect(BUTTON_PREV, GPIO.FALLING, callback=MPC.prev, bouncetime=300)

mpc = {}
series = []

#def helper_car_mongo_to_value(auto,wert):
#	global values
#	val = keyvalue.select("auto"+str(auto)+str(wert))
#	helper_check_key(values,"auto")
#	helper_check_key(values["auto"],auto)
#	helper_check_key(values["auto"][auto],wert)
#	if(values["auto"][auto][wert] != val):
#		values["auto"][auto][wert] = val
#		return True
#	else:
#		return False

def read_1wire(wid):
	file = open('/sys/bus/w1/devices/' + wid + '/w1_slave')
	filecontent = file.read()
	file.close()
	stringvalue = filecontent.split("\n")[1].split(" ")[9]
	return float(stringvalue[2:]) / 1000

def log_1wire():
	for key,adr in w1.items():
		value = read_1wire(adr)
		points = {
				"name": "w1",
				"columns": [key],
				"points": [[value]]
		}
		print(str(key) + ' | %5.3f C' % value)
		keyvalue.update("w1_"+key,value)
		log.append_series(points)

def log_disk():
	global series
	partitions = psutil.disk_partitions()
	for p in partitions:
		disk = psutil.disk_usage(p.mountpoint)
		points = {
			"name": "disk_usage",
			"columns": ["mount","used", "free", "percent", "host"],
			"points": [
				[p.mountpoint, disk.used, disk.free, disk.percent , hostname]
			]
		}
		#keyvalue.update("hdd_",disk.used)
		#keyvalue.update("cpu_temperatur",disk.free)
		#keyvalue.update("cpu_temperatur",disk.percent)
		log.append_series(points)

def log_cpu_temp():
	tstr = ""
	global series
	with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
		tstr = f.read()
	tfloat = float(tstr)
	tfloat = tfloat / 1000
	points = {
		"name": "cpu_temperatur",
		"columns": ["value", "host"],
		"points": [
			[tfloat, hostname]
		]
	}
	keyvalue.update("cpu_temperatur",tfloat)
	log.append_series(points)

def log_cpu_percent():
	global series
	cpu = psutil.cpu_percent(interval=1)
	points = {
		"name": "cpu_percent",
		"columns": ["value", "host"],
		"points": [
			[cpu, hostname]
		]
	}
	keyvalue.update("cpu_percent",cpu)
	log.append_series(points)


def log_mem():
	global series
	mem = psutil.virtual_memory()
	points = {
			"name": "mem_usage",
			"columns": ["used", "total", "percent", "host"],
			"points": [
			[mem.used, mem.total, mem.percent, hostname]
			]
	}
	keyvalue.update("mem_used",mem.used)
	keyvalue.update("mem_total",mem.total)
	keyvalue.update("mem_percent",mem.percent)
	series.append(points)

if(use_serial):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	time.sleep(3)

def serial_write(str):
	time.sleep(telegram_sleep)
	if(use_serial):
		#print "ON: " +  str
		ser.write(str)
	#else:
	#	print "OFF: " +  str


def send_mpd(id):
	global mpc
	song = MPC.song()[:24]
	song_status = MPC.title_status()
	status = MPC.mpd_status()
	if(song != mpc["song"] or id == -2):
		mpc["song"] = song
		if(id == 0 or id < 0):
			serial_write("mpd 0 "+ mpc["song"] + " \r")
	if(song_status != mpc["song_status"] or id == -2):
		mpc["song_status"] = song_status
		if(id == 1 or id < 0):
			serial_write("mpd 1 "+ mpc["song_status"]["title"] + " \r")
	if(status != mpc["status"] or id == -2):
		if(id == 2 or id < 0):
			mpc["status"] = status
			serial_write("mpd 2 V: " + mpc["status"]["volume"] + "%  RE: " + mpc["status"]["repeat"] +"  RE: " + mpc["status"]["random"] +"\r")

# thread!
def thread_send_values():
	value = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	def value_string(i, value, old_value):
		val = keyvalue.select(value)
		if(val != old_value):
			serial_write("value "+ str(i) +" "+ "%5.1f" % val + " \r")
			return val
		return old_value
	while True:
		time.sleep(1)
		try:
			value[0] = value_string(0,"w1_oel",			value[0])
			value[1] = value_string(1,"w1_bier",		value[1])
			value[2] = value_string(2,"cpu_temperatur",	value[2])
			value[3] = value_string(3,"w1_motor",		value[3])
			value[4] = value_string(4,"w1_aussen",		value[4])
			value[5] = value_string(5,"w1_innen",		value[5])
		except:
			print sys.exc_info()
			return False

#thread
def thread_log_system():
	while True:
		time.sleep(1)
		try:
			log_cpu_temp()
			log_mem()
			log_disk()
			log_cpu_percent()
		except:
			print sys.exc_info()
			return False

def thread_log_1wire():
	while True:
		try:
			log_1wire()
		except:
			print sys.exc_info()
			return False

def cleanup():

	if(use_serial):
		ser.close()
	GPIO.cleanup()

thValues = threading.Thread(target=thread_send_values)
thLogSystem = threading.Thread(target=thread_log_system)
thLog1Wire = threading.Thread(target=thread_log_1wire)
thValues.daemon = True
thLogSystem.daemon = True
thLog1Wire.daemon = True

try:
	mpc["song_status"] = MPC.title_status()
	mpc["status"] = MPC.mpd_status()
	mpc["song"] = MPC.song()[:24]
	send_mpd(-2)

	thValues.start()
	thLogSystem.start()
	thLog1Wire.start()
	while 1:

		#keyvalue.restore()
		log.write_series()
		#store_keyvalues()
		#gc.collect()


		#print mpc_get_status2()
		#print mpc_get_song()
		#print mpc_get_stats()
		time.sleep(circle_sleep)
		if lcd_seite == 0:
			# |   artist 1 - song 123    |
			# |  #12/24 1:24/4:31 (34%)  |
			# | V: 51%  RE: off  RA: off |
			#send_values()
			send_mpd(-1)
except KeyboardInterrupt:
	print "KeyboardInterrupt"	
except:
	print sys.exc_info()
	print "other error"	
finally:
	#thValues.terminate()
	#thLogSystem.terminate()
	#thLog1Wire.terminate()
	cleanup()
