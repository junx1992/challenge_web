#-*-coding:utf-8-*-
class MongoDB:
	def __init__(self):
		from pymongo import MongoClient
		self.con = MongoClient('localhost')
		self.db = self.con.challenge

db = MongoDB().db
register_team = db.video
a = register_team.find()
import hashlib
for item in a:
	print (item['_id'], item['teamname'])
	for member in item['member']:
		print(member['name'], member['email'], member['organization'])

	print('\n\n')
