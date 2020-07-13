#-*-coding:utf-8-*-
class MongoDB:
	def __init__(self):
		from pymongo import MongoClient
		self.con = MongoClient('localhost')
		self.db = self.con.challenge
mail_list = []
db = MongoDB().db
register_team = db.video
a = register_team.find()
import hashlib
our_num = 10
all_num = 0
fh = open('team.txt','w')
for item in a:
    all_num += 1
    print (item['_id'], item['teamname'])
    fh.write(str(item['teamname']))
    fh.write('\n')
    for member in item['member']:
        print(member['name'], member['email'], member['organization'])
        fh.write(str(member['name']))
        fh.write('\t')
        fh.write(str(member['email']))
        fh.write('\t')
        fh.write(str(member['organization']))
        fh.write('\n')
        mail_list.append(member['email'])
    print('\n\n')
    fh.write('\n\n\n')
fh.close()
print("All Num:", all_num)
print("All Clean Num:", all_num-our_num)
with open('email_list.txt', 'w') as fh:
    for email in mail_list:
        fh.write(email)
        fh.write('\n')
