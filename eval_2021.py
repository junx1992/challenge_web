#-*-coding:utf-8-*-
from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import json as js
from json import encoder
import argparse
import os

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pandas as pd
mail = 'junx1992@gmail.com'

class MongoDB:
	def __init__(self):
		from pymongo import MongoClient
		self.con = MongoClient('localhost')
		self.db = self.con.challenge

def send_email(mail_list, message, time):
    smtp = smtplib.SMTP('localhost')
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = Header("Pre-training-Video-Captioning-Challenge<root@auto-video-captions.top>")
    msg['To'] = Header(mail_list[0])
    msg['Subject'] = '[Pre-training-Video-Captioning-Challenge Evaluation Result Notice '+ time + ']'
    print (mail)
    try:
        smtp.sendmail("root@auto-video-captions.top", mail_list, msg.as_string())
        print('send email success')
        return 'ok'
    except:
        return 'error'
        print('send failed')

def unzip_folder(folder):
	result_files = os.listdir(folder)
	for result_name in result_files:
		result_file = os.path.join(folder, result_name)
		tar_folder = os.path.join(folder, result_name.replace('.zip', ''))
		if '_time' in result_name and '.zip' in result_name:
			if not os.path.exists(tar_folder):
				os.system('unzip {0} -d {1}'.format(result_file,tar_folder))

def get_team_id_mail_mapping():
    db = MongoDB().db
    register_team = db.video
    a = register_team.find()
    import hashlib
    name_mapping = {}
    for item in a:
        team_id = str(item['_id'])
        mail_list = []
        for member in item['member']:
            mail_list.append(str(member['email']))
        name_mapping[team_id] = mail_list
    return name_mapping

def load_json_evaluate(input):
    # load test groundtruth
    vname_label = {}
    gt_file = './tmp/groundtruth/cls_test_gt_list.csv'
    df_test = pd.read_csv(gt_file,sep=' ')
    vname = df_test['video_id']
    gt = df_test['label']
    assert len(vname) == len(gt)
    vname_gt = dict(zip(vname,gt))
    # load json
    correct = 0 
    with open(input,'r') as fr:
        pred = js.load(fr)
        version, result = pred['version'], pred['result']
        assert version == 'VERSION 1.3', 'version should be 1.3.'
        assert len(result) == len(vname), 'video prediction number should be 16554.'
        for v in result:
            vname = v['video_id'][:11]
            label = v['category_id']
            gt = vname_gt[vname]
            if label == gt: correct += 1
    accuracy = correct / len(result)
    print('top-1: %f'%accuracy)
    return accuracy

def caption_eval():
    annFile='./tmp/groundtruth/mm2021_test_sen.json'
    coco = COCO(annFile)
    folder = './tmp/result'

    unzip_folder(folder)
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
    #name_mapping = get_team_id_mail_mapping()
    count_mapping = {}
    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' not in sub_folder:
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time
            if not team_time_id in count_mapping:
                count_mapping[team_time_id] = 0 
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            if os.path.exists(performace_txt):
                count_mapping[team_time_id] += 1 

    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' not in sub_folder: 
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time 
            if not team_time_id in count_mapping:
                count_mapping[team_time_id] = 0            
            #mail_list = name_mapping[team_id]
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            except_txt = os.path.join(sub_folder, 'exception.txt')
            message = "Here is your evaluation result for " + time + " on track 1 \n"
            if not os.path.exists(performace_txt):
                if not os.path.exists(except_txt):
                    try:
                        if count_mapping[team_time_id] < 3:
                            resFiles = [resFile for resFile in os.listdir(sub_folder) if '.json' in resFile]
                            res_count = 0 
                            for resFile in resFiles:
                                if res_count < 3:
                                    print('Evaluate: ' + resFile)
                                    cocoRes = coco.loadRes(os.path.join(sub_folder, resFile))
                                    cocoEval = COCOEvalCap(coco, cocoRes)
                                    cocoEval.evaluate()
                                    with open(performace_txt, 'a') as fid:
                                        fid.write(resFile + ' ' + str(cocoEval.eval) + '\n')
                                        message += resFile + ' ' + str(cocoEval.eval) + '\n'
                                    res_count += 1
                            message += '\n\n'
                            message += 'Best,\n'
                            message += 'Organizing Committee'                
                            #send_email(mail_list, message, time)
                            #print('send email for success', mail_list)
                            count_mapping[team_time_id] += 1
                    except Exception as e:
                        with open(except_txt, 'w') as fh:
                            fh.write(str(e))
                        err_message = "Your Submitted file does not meet the standard requirement of our challenge. The sample submit file can be referred to http://auto-video-captions.top/static/resource/result.zip. [video_id should be same with the test json file]"
                        err_message += '\n\n'
                        err_message += 'Best,\n'
                        err_message += 'Organizing Committee'
                        #send_email(mail_list, message, time)  
                        #print('send email for fail', mail_list)                                            
                        print(str(e))
 


def class_eval():
    # annFile='./tmp/groundtruth/mm2020_test_sen.json'
    # coco = COCO(annFile)
    folder = './tmp/result'

    unzip_folder(folder)
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
    #name_mapping = get_team_id_mail_mapping()
    count_mapping = {}
    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' in sub_folder:
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time
            if not team_time_id in count_mapping:
                count_mapping[team_time_id] = 0 
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            if os.path.exists(performace_txt):
                count_mapping[team_time_id] += 1 

    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' in sub_folder: 
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time 
            if not team_time_id in count_mapping:
                count_mapping[team_time_id] = 0            
            #mail_list = name_mapping[team_id]
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            except_txt = os.path.join(sub_folder, 'exception.txt')
            message = "Here is your evaluation result for " + time + " on track 2 \n"
            if not os.path.exists(performace_txt):
                if not os.path.exists(except_txt):
                    try:
                        if count_mapping[team_time_id] < 3:
                            resFiles = [resFile for resFile in os.listdir(sub_folder) if '.json' in resFile]
                            res_count = 0 
                            for resFile in resFiles:
                                if res_count < 3:
                                    print('Evaluate: ' + resFile)
                                    # cocoRes = coco.loadRes(os.path.join(sub_folder, resFile))
                                    # cocoEval = COCOEvalCap(coco, cocoRes)
                                    # cocoEval.evaluate()
                                    result = load_json_evaluate(os.path.join(sub_folder, resFile))
                                    with open(performace_txt, 'a') as fid:
                                        fid.write(resFile + ' ' + str(result) + '\n')
                                        message += resFile + ' ' + str(result) + '\n'
                                    res_count += 1
                            message += '\n\n'
                            message += 'Best,\n'
                            message += 'Organizing Committee'                
                            #send_email(mail_list, message, time)
                            #print('send email for success', mail_list)
                            count_mapping[team_time_id] += 1
                    except Exception as e:
                        with open(except_txt, 'w') as fh:
                            fh.write(str(e))
                        err_message = "Your Submitted file does not meet the standard requirement of our challenge. The sample submit file can be referred to http://auto-video-captions.top/static/resource/result.zip. [video_id should be same with the test json file]"
                        err_message += '\n\n'
                        err_message += 'Best,\n'
                        err_message += 'Organizing Committee'
                        #send_email(mail_list, message, time)  
                        #print('send email for fail', mail_list)                                            
                        print(str(e))


if __name__=='__main__':
    while True:
        caption_eval()
        class_eval()