from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import json
from json import encoder
import argparse
import os

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--folder',   type=str,   default='',     help="result_folders")
    args = parser.parse_args()

    annFile='/export/home/xujun94/code/challenge_web/tmp/groundtruth/mm2020_test_sen.json'
    coco = COCO(annFile)
    folder = args.folder
    sub_folders = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
    for sub_folder in sub_folders:

        resFiles = [resFile for resFile in os.listdir(sub_folder) if '.json' in resFile]

        for resFile in resFiles:
            print('Evaluate: ' + resFile)
            cocoRes = coco.loadRes(os.path.join(sub_folder, resFile))
            cocoEval = COCOEvalCap(coco, cocoRes)
            cocoEval.evaluate()
            with open(os.path.join(sub_folder, 'performance.txt'), 'a') as fid:
                fid.write(resFile + ' ' + str(cocoEval.eval) + '\n')
