import psutil
import serial
import time
from subprocess import *
import os
import pymongo
from pymongo import MongoClient
from bson import BSON
from bson import json_util

mongo = MongoClient()
#mongo = MongoClient('mongodb://localhost:27017/')
db = mongo.rallye
values = db.values
mpd = db.mpd

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(3)
title = run_cmd('mpc current')[:22]
ser.write("mpd 0 "+ title + " \r")

# {{60.2,"OEL1",500.0},
# {66.5,"OEL2",500.0},
# {62.0,"RPI",60.0},
# {120.1,"Motor",500.0},
# {27.6,"Aussen",500.0},
# {23.4,"Innen",500.0}};

def update_mpd_to_db():
	run_cmd('mpc current')[:22]

while 1:
	time.sleep(1)
	value = psutil.cpu_percent()
	temp = run_cmd('mpc current')[:22]
	if(temp != title):
		title = temp
		ser.write("mpd 0 "+ title + " \r")

	ser.write("value 0 " + values.find_one({"name":request.json.get("Oel1")})["value"] + " \r")	 # OEL1
	ser.write("value 1 " + values.find_one({"name":request.json.get("Oel2")})["value"] + " \r")	 # OEL2
	ser.write("value 2 " + values.find_one({"name":request.json.get("RPI")})["value"] + " \r")  # RPI
	ser.write("value 3 " + values.find_one({"name":request.json.get("Motor")})["value"] + " \r")  # Motor
	ser.write("value 4 " + values.find_one({"name":request.json.get("Aussen")})["value"] + " \r")  # Aussen
	ser.write("value 5 " + values.find_one({"name":request.json.get("Innen")})["value"] + " \r")  # Innen
	print "value 0 " + str(value) + "\r"
ser.close()
