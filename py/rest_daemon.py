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

config = json.loads(open('config.json').read())
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

#es.indices.create(index='system-index', ignore=400)

def print_logger(str):
	print colored("logger:", 'cyan'), colored(str, 'magenta')

def log_cpu():
	cpu = psutil.cpu_percent(interval=1)
	#res = es.index(index="fileserv-index", doc_type='cpu', body={
    #	"name": "cpu_idle",
    #	"value": cpu,
    #	"@timestamp": datetime.utcnow()
	#})
	db_influx.write_points([{
		"name": "cpu_idle",
		"columns": ["value", "host"],
		"points": [
		[cpu, hostname]
		]
	}])
	print_logger("CPU -> val:" + str(cpu))

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

def thread_logger():
	while(1):
		log_cpu()
		log_mem()
		time.sleep(5)


# curl -i http://127.0.0.1:5002/api/v1.0/value
@app.route('/api/v1.0/ping', methods=['get'])
def get_ping():
	doc = values.find()
	return "OK", 201

@app.route('/api/v1.0/ping', methods=['post'])
def post_ping():
	doc = values.find()
	return "OK", 201

# curl -i http://127.0.0.1:5002/api/v1.0/value
@app.route('/api/v1.0/value', methods=['get'])
def get_values():
	doc = values.find()
	return json_util.dumps(doc, sort_keys=True, indent=4, default=json_util.default), 201


# curl -i http://127.0.0.1:5002/api/v1.0/value/aussen
@app.route('/api/v1.0/value/<string:name>', methods=['get'])
def get_value(name):
	doc = values.find_one({"name":name})
	return json_util.dumps(doc, sort_keys=True, indent=4, default=json_util.default), 201

# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"aussen", "value":123.2}' http://127.0.0.1:5002/api/v1.0/value
@app.route('/api/v1.0/value', methods=['POST'])
def post_value():
	if not request.json or not 'name' in request.json or not 'value' in request.json:
		abort(400)
	values.update({'name':request.json.get("name")},request.json,True)
	doc = values.find_one({"name":request.json.get("name")})
	return json_util.dumps(doc, sort_keys=True, indent=4, default=json_util.default), 201

if __name__ == '__main__':
	start_new_thread(thread_logger,())

	#app.run(host="192.168.3.184",port=5002,debug=True)
	app.run(port=5002,debug=True)

	#!/usr/bin/python


