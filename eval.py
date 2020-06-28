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
    resFiles = [resFile for resFile in os.listdir(args.folder) if '.json' in resFile]

    for resFile in resFiles:
        print('Evaluate: ' + resFile)
        cocoRes = coco.loadRes(os.path.join(args.folder, resFile))
        cocoEval = COCOEvalCap(coco, cocoRes)
        cocoEval.evaluate()
        with open(os.path.join(args.folder, 'performance.txt'), 'a') as fid:
            fid.write(resFile + ' ' + str(cocoEval.eval) + '\n')
