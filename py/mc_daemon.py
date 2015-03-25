#!/usr/bin/python
#
#music and control daemon

import psutil
import json
import serial
import time
from subprocess import *
import os
import pymongo
from pymongo import MongoClient
from bson import BSON
from bson import json_util

config = json.loads(open('../configs/aor_service.json').read())

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
	if(use_serial):
		ser.write(str)
		print str
	else:
		print str

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

def mpc_get_status():
	s =  mpc_cmd('')
	print s[0:6]
	if(s[0:6] != "volume"):
		a = s.split('\n')
		l = a[2]
	else:
		l = s
	return {"volume": l[7:10],"repeat": l[22:25],"random": l[36:39],"single": l[50:53],"consume": l[65:68]}

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
		print inc+length-len(playlist)
		for i in range(inc+length-len(playlist)+1):
			partlist.append(playlist[i])
	return partlist

while 1:
	#print mpc_get_status()
	#print mpc_get_song()
	#print mpc_get_stats()
	time.sleep(circle_sleep)
	if lcd_seite == 0:
		mpc_status = mpc_get_status()
		# |   artist 1 - song 123    |
		# |  #12/24 1:24/4:31 (34%)  |
		# | V: 51%  RE: off  RA: off |
		serial_write("mpd 0 "+ mpc_get_song()[:24] + " \r")
		#serial_write("mpd 1 V: " + " \r")
		time.sleep(telegram_sleep)
		serial_write("mpd 1 V: " + mpc_status["volume"] + "%  RE: " + mpc_status["repeat"] +"  RE: " + mpc_status["random"] +"\r")

if(use_serial):
	ser.close()
