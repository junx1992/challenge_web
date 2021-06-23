#-*-coding:utf-8-*-

from flask import Blueprint, request, jsonify, make_response, send_file, abort
from config import *
import os
api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
	form = request.form
	required = ['challenge_type', 'username', 'password', 'teamname', 'caption_name', 'caption_email', 'caption_organization', 'member_num']
	for item in required:
		if not item in form:
			return jsonify(res=PARAMETER_ERROR)

	challenge_type = form['challenge_type']
	username = form['username']
	password = form['password']
	teamname = form['teamname']

	if username == "" or len(password) < 6 or teamname == "":
		return jsonify(res=PARAMETER_ERROR)

	caption_name = form['caption_name']
	caption_email = form['caption_email']
	caption_organization = form['caption_organization']
	if 'track_id' in form:
		track_id = form['track_id']
	else:
		track_id = 0

	if caption_name == "" or caption_email == "" or caption_organization == "":
		return jsonify(res=PARAMETER_ERROR)

	member_num = int(form['member_num'])
	member = [{
		'name':caption_name,
		'email':caption_email,
		'organization':caption_organization
	}]
	for i in range(1, member_num):
		required = ['member%d_name'%i, 'member%d_email'%i, 'member%d_organization'%i]
		for item in required:
			if not item in form:
				return jsonify(res=PARAMETER_ERROR)

		member_name = form['member%d_name'%i]
		member_email = form['member%d_email'%i]
		member_organization = form['member%d_organization'%i]

		if member_name == "" or member_email == "" or member_organization == "":
			return jsonify(res=PARAMETER_ERROR)

		member.append({
			'name':member_name,
			'email':member_email,
			'organization':member_organization
			})

	from lib import check_team_member
	status, err, place = check_team_member(challenge_type, username, password, teamname, member, track_id)
	if status == False:
		if err == TEAM_NAME_UNAVALIABLE:
			return jsonify(res=TEAM_NAME_UNAVALIABLE)
		elif err == USER_NAME_UNAVALIABLE:
			return jsonify(res=USER_NAME_UNAVALIABLE)
		else:
			return jsonify(res=MEMBER_UNAVALIABLE, place=place)
	else:
		from lib import send_email
		import json
		msg = "Registration\n"
		for item in member:
			msg += "%s %s %s\n"%(item['name'],item['email'],item['organization'])
		send_email("junx1992@gmail.com", msg)
		print (msg)
		msg_data = "Dear Team " + teamname + "\n\n"
		msg_data += "Welcome to join in our challenge! This year, we provide two large-scale video pre-training datasets (ACTION and a Weakly-Supervised dataset) for solving the challenging but emerging vision-language pre-training task.\n\n"
		msg_data += "For the first track of pre-training for video captioning, the link for downloading video-sentence pairs in ACTION is at http://auto-video-captions.top/static/dataset/ACTION.annotation.json. Note that due to the copyright issue, we only provide the url link for each GIF officially and every team needs to crawl the GIFs by yourself.\n\n"
		msg_data += "Another option is that as we know, one team from SYSU has downloaded all the original GIFs and shared the data at pan.baidu (https://pan.baidu.com/s/17zhXiDL-MNHG3lyCObKu8w, pwd: lzf0) and Google Drive (https://drive.google.com/drive/folders/13ZRb9_yfjUCt3JfJ6q1ibAcXYlLBtoFg?usp=sharing). You can directly capitalize on the off-the-shelf data as well.\n\n"
		msg_data += "For the second track of pre-training for video categorization, the link for downloading videos in the Weakly-Supervised dataset and Downstream is at http://auto-video-captions.top/static/dataset/Video-Pretrain-Data.zip and http://auto-video-captions.top/static/dataset/Video-Categorization-Data.zip, respectively. Note that due to the copyright issue, we only provide the url link for each YouTube video officially and every team needs to crawl the videos by yourself.\n\n"
		msg_data += "Another option is that as we know, one team from USTC has downloaded all the original videos and shared the data at pan.baidu: the Weakly-Supervised dataset (https://pan.baidu.com/s/1PPTPGbdxnAregXW26rQ-9g, pwd: pjo2) and Downstream (https://pan.baidu.com/s/1SSOmUHi_jWOnsLctugtNwg, pwd: 6gj7). You can directly capitalize on the off-the-shelf data as well.\n\n"



		# msg_data += "============Pre-training data=============\n"
		# msg_data += "The link for downloading video-sentence pairs in Auto-captions on GIF is at http://auto-video-captions.top/static/dataset/pre-training.zip. Note that due to the copyright issue, we only provide the url link for each GIF officially and every team needs to crawl the GIFs by yourself. \n\n"
		# msg_data += "Another option is that as we know, one team from SYSU has downloaded all the original GIFs and shared the data at pan.baidu (https://pan.baidu.com/s/1oDLy86Msc05sB_VagYqyXg, pwd: 237m) and Google Drive (https://drive.google.com/drive/folders/1YXd2Qu1Nr_6l0ccgo9vN9NWlyWnXacXU?usp=sharing). You can directly capitalize on the off-the-shelf data as well.\n\n"

		# msg_data += "============Testing data================\n"
		# msg_data += "Meanwhile, the testing set has been released now. The link for downloading testing videos is at http://auto-video-captions.top/static/dataset/mm2020_test_no_sen.zip. Note that due to the copyright issue, we only provide the url link for each video officially and every team needs to crawl the videos by yourself.\n"
		# msg_data += "One team from SYSU has downloaded all the original testing videos and shared the data at pan.baidu (https://pan.baidu.com/s/1fCxixaC0dy8LyveynH9L-A, pwd: gyd5) and Google Drive (https://drive.google.com/file/d/1rssqYU6WvxxBw3OCXtSc6opsLmtbWfJM/view?usp=sharing). You can directly capitalize on the off-the-shelf data as well.\n\n"
		msg_data += "Best,\n"
		msg_data += "Organizing Committee"
		send_email(caption_email, msg_data)
		print (msg_data)

		resp = jsonify(res=SUCCESS)
		resp.set_cookie('session', place)
		return resp

@api.route('/update', methods=['POST'])
def update():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']
	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp
	teamid = teamid.split('&')[0]
	form = request.form
	required = ['challenge_type', 'teamname', 'caption_name', 'caption_email', 'caption_organization']
	for item in required:
		if not item in form:
			return jsonify(res=PARAMETER_ERROR)
	challenge_type = form['challenge_type']
	teamname = form['teamname']
	caption_name = form['caption_name']
	caption_email = form['caption_email']
	caption_organization = form['caption_organization']
	if caption_name == "" or caption_email == "" or caption_organization == "":
		return jsonify(res=PARAMETER_ERROR)
	if 'track_id' in form:
		track_id = form['track_id']
	member_num = int(form['member_num'])
	member = [{
		'name':caption_name,
		'email':caption_email,
		'organization':caption_organization
	}]
	for i in range(1, member_num):
		required = ['member%d_name'%i, 'member%d_email'%i, 'member%d_organization'%i]
		for item in required:
			if not item in form:
				return jsonify(res=PARAMETER_ERROR)

		member_name = form['member%d_name'%i]
		member_email = form['member%d_email'%i]
		member_organization = form['member%d_organization'%i]

		if member_name == "" or member_email == "" or member_organization == "":
			return jsonify(res=PARAMETER_ERROR)

		member.append({
			'name':member_name,
			'email':member_email,
			'organization':member_organization
			})

	from lib import update_team_member
	status, err, place = update_team_member(challenge_type, teamid, teamname, member)
	if status == True:
		return jsonify(res=SUCCESS)
	else:
		if err == TEAM_NAME_UNAVALIABLE:
			return jsonify(res=TEAM_NAME_UNAVALIABLE)
		elif err == USER_NAME_UNAVALIABLE:
			return jsonify(res=USER_NAME_UNAVALIABLE)
		elif err == TEAM_NOT_EXIST:
			return jsonify(res=TEAM_NOT_EXIST)
		else:
			return jsonify(res=MEMBER_UNAVALIABLE, place=place)

@api.route('/login', methods=['POST'])
def login():
	form = request.form
	required = ['challenge_type', 'username', 'password']
	for item in required:
		if not item in form:
			return jsonify(res=PARAMETER_ERROR)

	challenge_type = form['challenge_type']
	username = form['username']
	password = form['password']

	from lib import auth
	status, session = auth(challenge_type, username, password)
	if status == True:
		resp = jsonify(res=SUCCESS)
		resp.set_cookie('session', session)
		return resp
	else:
		return jsonify(res=USERNAME_OR_PASSWORD_ERROR)

@api.route('/logout', methods=['GET'])
def logout():
	resp = jsonify(res="00000")
	resp.delete_cookie('session')
	return resp

@api.route('/getinfo', methods=['GET'])
def getinfo():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_info_by_session
	status, info = get_info_by_session(session)
	if status == False:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp
	else:
		return jsonify(res=SUCCESS, info=info)

@api.route('/submit', methods=['POST'])
def submit():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp 

	teamid = teamid.replace('&', '_')

	files = request.files
	f = files['file']
	filename = f.filename
	filetype = filename.split('.')[-1]
	import time
	nowtime = time.strftime('%Y-%m-%d-%H-%M', time.localtime(int(time.time())))
	filename = teamid + '_time_' + nowtime + '.' + filetype
	import os
	#os.system("rm tmp/result/%s*"%teamid)
	f.save('tmp/result/' + filename)
	os.system("cp tmp/result/%s tmp/result/%s"%(filename, teamid + '.zip'))

	from lib import team_submit
	team_submit(teamid)
	folder = 'tmp/result/'
	return jsonify(res=SUCCESS)

@api.route('/submit_2', methods=['POST'])
def submit():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp 

	teamid = teamid.replace('&', '_')

	files = request.files
	f = files['file']
	filename = f.filename
	filetype = filename.split('.')[-1]
	import time
	nowtime = time.strftime('%Y-%m-%d-%H-%M', time.localtime(int(time.time())))
	filename = teamid + '_time_' + nowtime + '_track2.' + filetype
	import os
	#os.system("rm tmp/result/%s*"%teamid)
	f.save('tmp/result/' + filename)
	os.system("cp tmp/result/%s tmp/result/%s"%(filename, teamid + '_track2.zip'))

	from lib import team_submit_2
	team_submit_2(teamid)
	folder = 'tmp/result/'
	return jsonify(res=SUCCESS)


@api.route('/submission', methods=['GET'])
def submission():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		abort(404)
	teamid = teamid.replace('&', '_')
	if os.path.exists("tmp/result/%s.zip"%teamid):
		return send_file("tmp/result/%s.zip"%teamid)
	else:
		abort(404)

@api.route('/submission_2', methods=['GET'])
def submission():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		abort(404)
	teamid = teamid.replace('&', '_')
	if os.path.exists("tmp/result/%s_track2.zip"%teamid):
		return send_file("tmp/result/%s_track2.zip"%teamid)
	else:
		abort(404)

@api.route('/submit_report', methods=['POST'])
def submit_report():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp 

	teamid = teamid.replace('&', '_')

	files = request.files
	f = files['file']
	filename = f.filename
	filetype = filename.split('.')[-1]
	import time
	nowtime = time.strftime('%Y-%m-%d-%H-%M', time.localtime(int(time.time())))
	filename = teamid + '_time_' + nowtime + '.' + filetype
	import os
	#os.system("rm tmp/report/%s*"%teamid)
	f.save('tmp/report/' + filename)
	os.system("cp tmp/report/%s tmp/report/%s"%(filename, teamid + '.pdf'))

	from lib import team_submit_report_2
	team_submit_report_2(teamid)

	return jsonify(res=SUCCESS)

@api.route('/submission_report', methods=['GET'])
def submission_report():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		abort(404)
	teamid = teamid.replace('&', '_')
	if os.path.exists("tmp/report/%s.pdf"%teamid):
		return send_file("tmp/report/%s.pdf"%teamid)
	else:
		abort(404)


@api.route('/submit_report_2', methods=['POST'])
def submit_report():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		resp = jsonify(res=NOT_LOGIN)
		resp.delete_cookie('session')
		return resp 

	teamid = teamid.replace('&', '_')

	files = request.files
	f = files['file']
	filename = f.filename
	filetype = filename.split('.')[-1]
	import time
	nowtime = time.strftime('%Y-%m-%d-%H-%M', time.localtime(int(time.time())))
	filename = teamid + '_time_' + nowtime + '_track2.' + filetype
	import os
	#os.system("rm tmp/report/%s*"%teamid)
	f.save('tmp/report/' + filename)
	os.system("cp tmp/report/%s tmp/report/%s"%(filename, teamid + '_track2.pdf'))

	from lib import team_submit_report
	team_submit_report(teamid)

	return jsonify(res=SUCCESS)

@api.route('/submission_report_2', methods=['GET'])
def submission_report():
	cookies = request.cookies
	if not 'session' in cookies:
		return jsonify(res=NOT_LOGIN)
	session = cookies['session']

	from lib import get_teamid_by_session
	teamid = get_teamid_by_session(session)
	if teamid == None:
		abort(404)
	teamid = teamid.replace('&', '_')
	if os.path.exists("tmp/report/%s_track2.pdf"%teamid):
		return send_file("tmp/report/%s_track2.pdf"%teamid)
	else:
		abort(404)


@api.route('/allteam', methods=['GET'])
def allteam():
	args = request.args
	if not 'token' in args or not 'challenge_type' in args:
		return jsonify(res=PARAMETER_ERROR)
	token = args['token']
	if token != 'msramsmbest':
		return jsonify(res=PARAMETER_ERROR)
	challenge_type = args['challenge_type']
	from lib import get_all_team
	team = get_all_team(challenge_type)
	return jsonify(res=SUCCESS, team=team)

@api.route('/changepassword', methods=['POST'])
def changepassword():
	form = request.form
	required = ['challenge_type', 'team_name', 'caption_name', 'caption_email']
	for item in required:
		if not item in required:
			return jsonify(res=PARAMETER_ERROR)

	challenge_type = form['challenge_type']
	team_name = form['team_name']
	caption_name = form['caption_name']
	caption_email = form['caption_email']

	from lib import check_and_send_reset_password_email
	status = check_and_send_reset_password_email(challenge_type, team_name, caption_name, caption_email)
	if status == True:
		return jsonify(res=SUCCESS)
	else:
		return jsonify(res=CAPTION_NAME_EMAIL_NOT_MATCH)

@api.route('/getresetinfo', methods=['GET'])
def getresetinfo():
	args = request.args
	if not 'token' in args or not 'challenge_type' in args:
		return jsonify(res=PARAMETER_ERROR)

	token = args['token']
	challenge_type = args['challenge_type']

	from lib import get_reset_info_by_token
	status, info = get_reset_info_by_token(token, challenge_type)
	if status == True:
		return jsonify(res=SUCCESS, info=info)
	else:
		return jsonify(res=INVALID_TOKEN)

@api.route('/reset', methods=['POST'])
def reset():
	form = request.form
	required = ['challenge_type', 'token', 'username', 'teamname', 'captionname', 'password']
	for item in required:
		if not item in required:
			return jsonify(res=PARAMETER_ERROR)

	challenge_type = form['challenge_type']
	token = form['token']
	username = form['username']
	teamname = form['teamname']
	captionname = form['captionname']
	password = form['password']

	from lib import reset_password_by_token
	status, code = reset_password_by_token(challenge_type, token, username, teamname, captionname, password)
	if status == True:
		resp = jsonify(res=SUCCESS)
		resp.set_cookie('session', code)
		return resp
	else:
		return jsonify(res=INVALID_TOKEN)
