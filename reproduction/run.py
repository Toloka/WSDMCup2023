import pandas as pd
import cv2
import wget
import shutil
import os
from tqdm.auto import tqdm
from joblib import Parallel, delayed
import numpy as np
import torch
from PIL import Image
import clip
import subprocess
import matplotlib.pyplot as plt


def get_iou(bb1, bb2):
    # Taken from https://stackoverflow.com/a/42874377
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou


def process_image(img_path, bb_prediction, preprocess, device):
    np_img = cv2.imread(img_path)
    imgs = []
    with open(bb_prediction) as f:
        lines = f.readlines()
    bbs = [list(map(float, line.split(' ')[1:5])) for line in lines]
    bbs_processed = []
    for bb in bbs:
        y, x, h, w = bb
        height, width, channels = np_img.shape
        x *= height
        w *= height
        y *= width
        h *= width
        crop = np_img[int(x - w // 2):int(x + w // 2), int(y - h // 2):int(y + h // 2), :]
        imgs.append(preprocess(Image.fromarray(crop)).unsqueeze(0).to(device))
        bbs_processed.append({'y1': int(x - w // 2), 'y2': int(x + w // 2), 'x1': int(y - h // 2), 'x2': int(y + h // 2)})
    return imgs, bbs_processed

def predict(img_url, question, preprocess, model, device='cuda'):
    img_path = os.path.join('/mnt/data/imgs', img_url)
    bb_prediction = os.path.join('yolor', 'inference', 'output', img_url).replace('.jpg', '.txt')
    imgs, bbs_processed = process_image(img_path, bb_prediction, preprocess, device)
    
    text = clip.tokenize([question]).to(device)
    probs = []
    for img in imgs:
        with torch.no_grad():
            logits_per_image, logits_per_text = model(img, text)
            probs.append(logits_per_image.softmax(dim=-1).cpu().numpy()[0][0])
    
    return bbs_processed[np.argmax(probs)]


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)

    train = pd.read_csv('/mnt/data/test.csv')
    print(train.head())

    os.chdir('yolor')
    command = "python detect.py --source /mnt/data/imgs --cfg cfg/yolor_p6.cfg --weights ../yolor_p6.pt --conf 0.1 --save-txt --img-size 1280 --device 0'"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.chdir('..')

    predictions = []
    n_imgs = 0
    total_iou = 0.0
    model, preprocess = clip.load("ViT-B/32", device=device)
    progress = tqdm(train.iterrows(), total=len(train))
    for _, row in progress:
        img_url = row['image']
        question = row['question']
        try:
            bb_predicted = predict(img_url, question, preprocess, model, device)
        except Exception as e:
            print(e)
            continue
        gt_bb = {'x1': row['left'], 'y1': row['top'], 'x2': row['right'], 'y2': row['bottom']}
        total_iou += get_iou(gt_bb, bb_predicted)
        n_imgs += 1
        progress.set_description(f'IoU: {round(total_iou / n_imgs * 100, 2)}')
        
        left = bb_predicted['x1']
        top = bb_predicted['y1']
        right = bb_predicted['x2']
        bottom = bb_predicted['y2']
        predictions.append([img_url, left, top, right, bottom])
    predictions = pd.DataFrame(predictions, columns=['image', 'left', 'top', 'right', 'bottom'])

    predictions.to_csv('/mnt/output/answer.csv', index=None)

if __name__ == '__main__':
    main()
