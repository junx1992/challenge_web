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
our_num = 8
all_num = 0
for item in a:
    all_num += 1
    print (item['_id'], item['teamname'])
    for member in item['member']:
        print(member['name'], member['email'], member['organization'])
    print('\n\n')
print("All Num:", all_num)
print("All Clean Num:", all_num-our_num)
