#!/usr/bin/python
#
# Status: Tested
#
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
#from elasticsearch import Elasticsearch
from flask import request
from bson import BSON
from bson import json_util
import time
from datetime import datetime
#from influxdb import InfluxDBClient
from influxdb.influxdb08 import InfluxDBClient
import psutil
import json
from thread import start_new_thread
from termcolor import colored

mongo = MongoClient()
#mongo = MongoClient('mongodb://localhost:27017/')

config = json.loads(open('../configs/aor_service.json').read())
db_influx = InfluxDBClient(config['influx']['host'],
	config['influx']['port'],
	config['influx']['user'],
	config['influx']['pw'],
	config['influx']['db'])

db_mongo = mongo.rallye
values = db_mongo.values
app = Flask(__name__)
#es = Elasticsearch()

hostname = config['hostname']
logging = True

#es.indices.create(index='system-index', ignore=400)

def print_logger(str):
	if(logging):
		print colored("logger:", 'cyan'), colored(str, 'magenta')

def log_disk():
	partitions = psutil.disk_partitions()
	for p in partitions:
		disk = psutil.disk_usage(p.mountpoint)
		print_logger("DISK -> " + p.mountpoint +  " :" + str(disk))
		db_influx.write_points([{
			"name": "disk_usage",
			"columns": ["mount","used", "free", "percent", "host"],
			"points": [
				[p.mountpoint, disk.used, disk.free, disk.percent , hostname]
			]
		}])

def log_cpu_temp():
	tstr = ""
	with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
		tstr = f.read()
	tfloat = float(tstr)
	tfloat = tfloat / 1000
	db_influx.write_points([{
		"name": "cpu_temperatur",
		"columns": ["value", "host"],
		"points": [
			[tfloat, hostname]
		]
	}])
	print_logger("CPU -> temp:" + str(tfloat))

def log_cpu_percent():
	cpu = psutil.cpu_percent(interval=1)
	#res = es.index(index="fileserv-index", doc_type='cpu', body={
    #	"name": "cpu_idle",
    #	"value": cpu,
    #	"@timestamp": datetime.utcnow()
	#})
	db_influx.write_points([{
		"name": "cpu_percent",
		"columns": ["value", "host"],
		"points": [
			[cpu, hostname]
		]
	}])
	print_logger("CPU -> percent:" + str(cpu))

def log_mem():
	mem = psutil.virtual_memory()
	#res = es.index(index="fileserv-index", doc_type='memory', body={
    #	"name": "mem_usage",
    #	"used": mem.used/1024/1024,
    #	"total": mem.total/1024/1024,
    #	"percent": mem.percent/1024/1024,
    #	"@timestamp": datetime.utcnow()
	#})
	db_influx.write_points([{
		"name": "mem_usage",
		"columns": ["used", "total", "percent", "host"],
		"points": [
		[mem.used, mem.total, mem.percent, hostname]
		]
	}])
	print_logger("RAM -> used:" + str(mem.used/1024/1024) + "MB")

while(True):
	log_cpu_percent()
	log_cpu_temp()
	log_mem()
	log_disk()
	#time.sleep(1)



