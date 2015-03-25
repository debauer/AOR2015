#!/usr/bin/python
#
# Status: Tested
#
import psutil
import json
import sys
import requests
import requests.exceptions
import time
import gc
from flask import Flask, jsonify, request
import pymongo
from bson import BSON
from bson import json_util
from datetime import datetime
#from influxdb import InfluxDBClient
from influxdb.influxdb08 import InfluxDBClient
from influxdb.influxdb08.client import InfluxDBClientError
from thread import start_new_thread
from termcolor import colored

config = json.loads(open('../configs/aor_service.json').read())

logging_info = config['logging']['logger']['info']
logging_error = config['logging']['logger']['error']
store_mongo = config['store']['mongo']
store_influx = config['store']['influx']
store_redis = config['store']['redis']
store_rrd = config['store']['rrd']
hostname = config['hostname']

if(store_mongo):
	mongo = pymongo.MongoClient()
	#mongo = MongoClient('mongodb://localhost:27017/')
	db_mongo = mongo.rallye
	values = db_mongo.values

#if(store_keyvalue == "redis"):
if(store_influx):
	db_influx = InfluxDBClient(config['influx']['host'],config['influx']['port'],config['influx']['user'],config['influx']['pw'],config['influx']['db'])

#app = Flask(__name__)

#es.indices.create(index='system-index', ignore=400)

series = []

def print_logger(str):
	if(logging_info):
		print colored("logger:", 'cyan'), colored(str, 'magenta')

def print_logger_error(str):
	if(logging_error):
		print colored("error:", 'red'), colored(str, 'magenta')

def print_influx_ConnectionError():
	print_logger_error("INFLUX ConnectionError")

def print_influx_ClientError():
	print_logger_error("INFLUX ClientError")

def influx_write_series():
	global series
	try:
		db_influx.write_points(series)
		series = []
	except InfluxDBClientError:
		print_influx_ClientError()
	except requests.exceptions.ConnectionError:
		print_influx_ConnectionError()

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
		series.append(points)
		print_logger("DISK -> " + p.mountpoint +  " :" + str(disk))

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
	print_logger("CPU -> temp:" + str(tfloat))
	series.append(points)

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
	series.append(points)
	print_logger("CPU -> percent:" + str(cpu))


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
	series.append(points)
	print_logger("RAM -> used:" + str(mem.used/1024/1024) + "MB")


try:

	print colored("==========================================", 'red')
	print colored("AOR Logger Script running", 'magenta')
	print colored("Autor: ", 'magenta') + colored("David 'debauer' Bauer", 'white')
	print colored("==========================================", 'red')
	while(True):
		log_cpu_percent()
		log_cpu_temp()
		log_mem()
		log_disk()
		influx_write_series()
		gc.collect()
		#time.sleep(1)

except (SystemExit):
	print " "
	print colored("SystemExit: stop script", "red")
	sys.exit()
except (KeyboardInterrupt):
	print " "
	print colored("KeyboardInterrupt: stop script", "red")
	sys.exit()


