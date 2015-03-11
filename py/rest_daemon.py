#!/usr/bin/python
#
# Status: Tested
#
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
from flask import request
from bson import BSON
from bson import json_util

mongo = MongoClient()
#mongo = MongoClient('mongodb://localhost:27017/')

db = mongo.rallye
values = db.values
app = Flask(__name__)

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
	#app.run(host="192.168.3.184",port=5002,debug=True)
	app.run(port=5002,debug=True)