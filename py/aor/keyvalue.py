from subprocess import *
import os,sys

class KeyValue(object):

	store_mongo = False
	store_redis = False
	mongo_values = {}
	values = {}
	values["cpu"] = {}
	values["ram"] = {}
	values["mpd"] = {}
	values["1wire"] = {}
	values["disk"] = {}

	def __init__(self, mongo = True, redis = False):
		self.store_mongo = mongo
		self.store_redis = redis
		if(mongo):
			import pymongo
			self.mongo = pymongo.MongoClient()
			#mongo = MongoClient('mongodb://localhost:27017/')
			self.mongo_db = self.mongo.rallye
			self.mongo_values = self.mongo_db.values
	
	def update(self, key,value):
		if(self.store_mongo):
			self.mongo_values.update({'key':key},{"key": key,"value":value},True)
	
	def select(self, key):
		try:
			if(self.store_mongo):
				s = self.mongo_values.find_one({"key":key})
				if s:
					return s["value"]
				else:
					return 0.0
			else:
				return 0.0
		except:
			print sys.exc_info()

#	def store_one(self, group, key):
#		self.check_key(values,group)
#		self.check_key(values[group],key)
#		self.update(group + "_" + key,	values[group][key])
#	
#	def restore_one(self, group, key):
#		self.check_key(values,group)
#		self.check_key(values[group],key)
#		values[group][key]	= self.select(group + "_" + key)
#
#	def check_key(dic,key):
#		if not key in dic:
#			dic[key] = {}
#
#	def store():
#		global series,values
#		for key,value in keyvalues.items():
#			store_one(key,value)
#
#	def restore():
#		global series,values
#		for key,value in keyvalues.items():
#			restore_one(key,value)