import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os 
mail = 'junx1992@gmail.com'
mail_2 = 'panyw.ustc@gmail.com'

mail_sb = '985776482@qq.com'

mail_sb_2 = '442720389@qq.com'

class MongoDB:
	def __init__(self):
		from pymongo import MongoClient
		self.con = MongoClient('localhost')
		self.db = self.con.challenge

def send_email(mail_list, message, time):
    smtp = smtplib.SMTP('localhost')
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = Header("Pre-training-Video-Understanding-Challenge<root@auto-video-captions.top>")
    if mail_list[0] == 'jim_wang2014@163.com':
        mail_list[0] = mail_sb
    if mail_list[0] == 'huang-yq17@mails.tsinghua.edu.cn':
        mail_list[0] = mail_sb_2
    msg['To'] = Header(mail_list[0])
    msg['Subject'] = '[Pre-training-Video-Understanding-Challenge Evaluation Result Notice '+ time + ']'
    print (mail)
    try:
        smtp.sendmail("root@auto-video-captions.top", mail_list, msg.as_string())
        print('send email success')
        return 'ok'
    except Exception as e:
        print('send failed')
        print(str(e))
        return 'error'

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

def track_1():
    folder = './tmp/result'
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]

    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' not in sub_folder: 
            name_mapping = get_team_id_mail_mapping()
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time        
            mail_list = name_mapping[team_id]
            mail_list.append(mail)
            mail_list.append(mail_2)
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            except_txt = os.path.join(sub_folder, 'exception.txt')
            message = "Here is your evaluation result for " + time + " on track 1. \n\n"
            send_txt = os.path.join(sub_folder, 'send.txt')
            if os.path.exists(performace_txt) and not os.path.exists(send_txt) and not os.path.exists(except_txt):
                with open(performace_txt) as fh:
                    data = fh.read()
                    message += data 
                    message += '\n'
                message += '\n\n'
                message += 'Best, \n'
                message += 'Organizaing Committee'

                try: 
                    send_email(mail_list, message, time)
                    print('send email for success', mail_list)

                    with open(send_txt, 'w') as fh:
                        fh.write('send success!')
                except Exception as e:
                    with open(except_txt, 'w') as fh:
                        fh.write(str(e))

def track_2():
    folder = './tmp/result'
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]

    for sub_folder in sub_folders:
        if '_video_time_' in sub_folder and 'track2' in sub_folder: 
            name_mapping = get_team_id_mail_mapping()
            base_name = os.path.basename(sub_folder)
            index = base_name.index('_video_time')
            team_id = base_name[0:index]
            time = base_name[index+12:]
            day_time = time[0:10]    
            team_time_id = team_id + '_' +day_time        
            mail_list = name_mapping[team_id]
            mail_list.append(mail)
            mail_list.append(mail_2)
            performace_txt = os.path.join(sub_folder, 'performance2.txt')
            except_txt = os.path.join(sub_folder, 'exception.txt')
            message = "Here is your evaluation result for " + time + " on track 2 \n"
            send_txt = os.path.join(sub_folder, 'send.txt')
            if os.path.exists(performace_txt) and not os.path.exists(send_txt) and not os.path.exists(except_txt):
                with open(performace_txt) as fh:
                    data = fh.read()
                    message += data 
                    message += '\n'
                message += '\n\n'
                message += 'Best, \n'
                message += 'Organizaing Committee'

                try: 
                    send_email(mail_list, message, time)
                    print('send email for success', mail_list)

                    with open(send_txt, 'w') as fh:
                        fh.write('send success!')
                except Exception as e:
                    with open(except_txt, 'w') as fh:
                        fh.write(str(e))

if __name__=='__main__':
    track_1()
    track_2()