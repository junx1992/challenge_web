import os 
import json

track_1_result = []
track_2_result = []


def parse_track_1(file_path, team_id, time):
    with open(file_path) as fh:
        for line in fh.readlines():
            line = line.strip()
            items = line.split('{')
            result_name = items[0].replace(' ', '')
            result_string = '{' + items[1].replace("'", '"')
            print(result_name)
            print(result_string)
            result = json.loads(result_string)
            track_1_result.append({ 'team_id': team_id, 
                                    'time': time,
                                    'result_name': result_name,
                                    'Bleu_1': result['Bleu_1'],
                                    'Bleu_2': result['Bleu_2'],
                                    'Bleu_3': result['Bleu_3'],
                                    'Bleu_4': result['Bleu_4'],
                                    'METEOR': result['METEOR'],
                                    'CIDEr': result['CIDEr'],
                                    'ROUGE_L': result['ROUGE_L'],
                                    'SPICE': result['SPICE']
                                    })
            


def parse_track_2(file_path, team_id, time):
    with open(file_path) as fh:
        for line in fh.readlines():
            line = line.strip()
            items = line.split(' ')
            result_name = items[0]
            result = items[1]
            track_2_result.append({
                'team_id': team_id,
                'time': time,
                'result_name': result_name,
                'top-1': result
            })
    


base_folder = './tmp/result/'
sub_folders = [os.path.join(base_folder, o) for o in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder,o))]

## track 1 ##
for sub_folder in sub_folders:
    if '_video_time_' in sub_folder and 'track2' not in sub_folder: 
        base_name = os.path.basename(sub_folder)
        index = base_name.index('_video_time')
        team_id = base_name[0:index]
        time = base_name[index+12:]
        performace_txt = os.path.join(sub_folder, 'performance2.txt')
        if os.path.exists(performace_txt):
            parse_track_1(performace_txt, team_id, time)


## track 2 ##
for sub_folder in sub_folders:
    if '_video_time_' in sub_folder and 'track2' in sub_folder: 
        base_name = os.path.basename(sub_folder)
        index = base_name.index('_video_time')
        team_id = base_name[0:index]
        time = base_name[index+12:]
        performace_txt = os.path.join(sub_folder, 'performance2.txt')
        if os.path.exists(performace_txt):
            parse_track_2(performace_txt, team_id, time)

result_1_file = os.path.join(base_folder, 'result_1.txt')
result_2_file = os.path.join(base_folder, 'result_2.txt')

with open(result_1_file, 'w') as fh:
    for value in track_1_result:
        fh.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n'
        .format(value['team_id'], value['time'], value['result_name'], value['Bleu_1'], value['Bleu_2'], value['Bleu_3'], value['Bleu_4'], 
                value['METEOR'], value['CIDEr'], value['ROUGE_L'], value['SPICE']))

with open(result_2_file, 'w') as fh:
    for value in track_2_result:
        fh.write('{0}\t{1}\t{2}\t{3}\n'
        .format(value['team_id'], value['time'], value['result_name'], value['top-1']))
