from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import json
from json import encoder
import argparse
import os

black_id = '5e72f8d5718d130c92d3130c'

def unzip_folder(folder):
	result_files = os.listdir(folder)
	for result_name in result_files:
		result_file = os.path.join(folder, result_name)
		tar_folder = os.path.join(folder, result_name.replace('.zip', ''))
		if '_time' in result_name and '.zip' in result_name:
			if not os.path.exists(tar_folder):
				os.system('unzip {0} -d {1}'.format(result_file,tar_folder))

if __name__=='__main__':
    annFile='./tmp/groundtruth/mm2020_test_sen.json'
    coco = COCO(annFile)
    folder = './tmp/result'
    unzip_folder(folder)
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
    for sub_folder in sub_folders:
        performace_txt = os.path.join(sub_folder, 'performance.txt')
        if black_id in sub_folder:
            continue
        if not os.path.exists(performace_txt):
            resFiles = [resFile for resFile in os.listdir(sub_folder) if '.json' in resFile]
            for resFile in resFiles:
                print('Evaluate: ' + resFile)
                cocoRes = coco.loadRes(os.path.join(sub_folder, resFile))
                cocoEval = COCOEvalCap(coco, cocoRes)
                cocoEval.evaluate()
                with open(performace_txt, 'a') as fid:
                    fid.write(resFile + ' ' + str(cocoEval.eval) + '\n')
