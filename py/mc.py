#!/usr/bin/python
#
#music and control daemon

from subprocess import *
import os,sys,time,serial,json,psutil
import pymongo
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import RPi.GPIO as GPIO

import logging
import logging.handlers
import argparse

# Deafults
LOG_FILENAME = "/var/log/aor/mc.log"
LOG_LEVEL = logging.DEBUG  # Could be e.g. "DEBUG" or "WARNING"

parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
 
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
	def __init__(self, logger, level):
		"""Needs a logger and a logger level."""
		self.logger = logger
		self.level = level
 
	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())
 
# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

config = json.loads(open('/home/debauer/AOR2015/configs/aor_service.json').read())

logging_info = config['logging']['logger']['info']
logging_error = config['logging']['logger']['error']
store_mongo = config['store']['mongo']
store_influx = config['store']['influx']
store_redis = config['store']['redis']
store_rrd = config['store']['rrd']
playlist_lines = config['music']['playlist_lines']
hostname = config['hostname']
circle_sleep = int(config['circle_sleep'])
telegram_sleep = float(config['telegram_sleep'])

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

mpc = {}

if(store_mongo):
	import pymongo
	mongo = pymongo.MongoClient()
	#mongo = MongoClient('mongodb://localhost:27017/')
	mongo_db = mongo.rallye
	mongo_values = mongo_db.values



def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

if(use_serial):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	time.sleep(3)

def mpc_cmd(cmd):
	return run_cmd('mpc ' + cmd)

def update_mpd_to_db():
	run_cmd('mpc current')[:22]

def serial_write(str):
	time.sleep(telegram_sleep)
	if(use_serial):
		print "ON: " +  str
		ser.write(str)
	else:
		print "OFF: " +  str

def mpc_get_stats():
	s =  mpc_cmd('stats')
	l = s.split('\n')
	return {"artists": int(l[0][8:]),
			"albums": int(l[1][7:]),
			"songs": int(l[2][6:]),
			"play_time": l[4][10:],
			"uptime": l[5][7:],
			"db_updated": l[6][11:],
			"db_play_time": l[7][13:]
		}

def mpc_get_song():
	return run_cmd('mpc current')

def mpc_get_status1():
	s =  mpc_cmd('')
	if(s[0:6] != "volume"):
		a = s.split('\n')
		d = a[1]
	else:
		d = ""
	status = {}
	if(d!=""):
		status["position"] = d[11:16] 
		status["time"] = d[19:28]
		if(d[:9] == "[paused]"):
			status["title"] = d[10:]
		elif(d[:9] == "[playing]"):
			status["title"] = d[11:]
		else:
			status["title"] = " "
	else:
		status["title"] = " "
		status["position"] = "asd" 
		status["time"] = "00:00:00"
	#print status["title"]
	return status

def mpc_get_status2():
	s =  mpc_cmd('')
	if(s[0:6] != "volume"):
		a = s.split('\n')
		l = a[2]
	else:
		l = s
	status = {"volume": l[7:10],"repeat": l[22:25],"random": l[36:39],"single": l[50:53],"consume": l[65:68],"position": "xx/xx","title": ""}
 	return status

def cleanup():
	if(use_serial):
		ser.close()
	GPIO.cleanup()

def mpc_get_playlist(inc,length = 4):
	p =  mpc_cmd('playlist')
	playlist = p.split('\n')
	partlist = []
	if(inc>=len(playlist)):
		inc = 0
	if(len(playlist)> inc+length):
		for i in range(inc,inc+length):
			partlist.append(playlist[i])
	else:
		for i in range(inc,len(playlist)):
			partlist.append(playlist[i])
		#print inc+length-len(playlist)
		for i in range(inc+length-len(playlist)+1):
			partlist.append(playlist[i])
	return partlist

def mongo_select(key):
	if(store_mongo):
		s = mongo_values.find_one({"key":key})
		if s:
			return s["value"]
		else:
			return ""

def serial_send_mpd(id):
	global mpc
	song = mpc_get_song()[:24]
	song_status = mpc_get_status1()
	status = mpc_get_status2()
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

def serial_send_values():
	if(store_mongo):
		temperatur = mongo_select("cpu_temperatur")
		temperatur_format = "{:4.1f}".format(temperatur)
		serial_write("value 2 "+ temperatur_format + " \r")

def mpc_next(channel):
	mpc_cmd("next")
	print("Button next pressed")

def mpc_prev(channel):
	mpc_cmd("prev")
	print("Button prev pressed")

GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=mpc_next, bouncetime=300)
GPIO.add_event_detect(BUTTON_PREV, GPIO.FALLING, callback=mpc_prev, bouncetime=300)

try:
	mpc["song_status"] = mpc_get_status1()
	mpc["status"] = mpc_get_status2()
	mpc["song"] = mpc_get_song()[:24]
	serial_send_mpd(-2)
	while 1:
		#print mpc_get_status2()
		#print mpc_get_song()
		#print mpc_get_stats()
		time.sleep(circle_sleep)
		if lcd_seite == 0:
			# |   artist 1 - song 123    |
			# |  #12/24 1:24/4:31 (34%)  |
			# | V: 51%  RE: off  RA: off |
			serial_send_values()
			serial_send_mpd(-1)

except KeyboardInterrupt:
	print "KeyboardInterrupt"

except:
	print sys.exc_info()
	print "other error"

finally:
    cleanup()
