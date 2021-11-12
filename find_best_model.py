# app.py
import itertools
import pickle

import cv2
import imutils
from imutils.contours import sort_contours
import numpy as np
import torch

from models import CharRecogModel


class_list = None
with open('models/class_list.pkl', 'rb') as class_list_file:
    class_list = pickle.load(class_list_file)

device = 'cpu'
char_recog_path = 'models/char_recog.pt'
char_recog_model = CharRecogModel(len(class_list))
char_recog_model.load_state_dict(torch.load(char_recog_path))
char_recog_model = char_recog_model.to(device)
char_recog_model.eval()

sample_dataset = {
    'data/test_samples/test_img_2.jpeg': ('harshan', None),
    'data/test_samples/test_img_3.jpeg': ('pro', None),
    'data/test_samples/test_img_4.jpeg': ('legend', None),
    'data/test_samples/test_img_5.jpeg': ('legend', None),
    'data/test_samples/test_img_6.jpeg': ('legend', None)
}

kernel_3_3 = np.ones((3, 3), np.uint8)
kernel_5_5 = np.ones((5, 5), np.uint8)

all_funcs = [
    # ('erode_3-3_1', lambda img: cv2.erode(img, kernel_3_3, iterations=1)),
    ('erode_5-5_1', lambda img: cv2.erode(img, kernel_5_5, iterations=1)),
    # ('erode_3-3_3', lambda img: cv2.erode(img, kernel_3_3, iterations=3)),
    ('erode_5-5_3', lambda img: cv2.erode(img, kernel_5_5, iterations=3)),
    # ('dilate_3-3_1', lambda img: cv2.dilate(img, kernel_3_3, iterations=1)),
    ('dilate_5-5_1', lambda img: cv2.dilate(img, kernel_5_5, iterations=1)),
    # ('dilate_3-3_3', lambda img: cv2.dilate(img, kernel_3_3, iterations=3)),
    ('dilate_5-5_3', lambda img: cv2.dilate(img, kernel_5_5, iterations=3)),
    ('thresh_bin', lambda img: cv2.threshold(img, 0, 255,
                                             cv2.THRESH_BINARY |
                                             cv2.THRESH_OTSU)[1]),
    # ('thresh_bin_inv', lambda img: cv2.threshold(img, 0, 255,
    #                                              cv2.THRESH_BINARY_INV |
    #                                              cv2.THRESH_OTSU)[1]),
    ('gauss_3-3_0', lambda img: cv2.GaussianBlur(img, (3, 3), 0)),
    # ('gauss_5-5_0', lambda img: cv2.GaussianBlur(img, (5, 5), 0)),
    ('median_3', lambda img: cv2.medianBlur(img, 3)),
    # ('median_5', lambda img: cv2.medianBlur(img, 5))
]


def get_character_segments(image, funcs):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for _, func in funcs:
        image = func(image)

    canny = cv2.Canny(image, 30, 150)
    cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        cnts = sort_contours(cnts, method="left-to-right")[0]

    chars = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        roi = image[y:y + h, x:x + w]
        thresh = cv2.threshold(roi, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        (tH, tW) = thresh.shape
        try:
            if tW > tH:
                thresh = imutils.resize(thresh, width=28)
            else:
                thresh = imutils.resize(thresh, height=28)
        except:
            print('H W = ', tH, tW)
            return []

        (tH, tW) = thresh.shape
        dX = int(max(0, 28 - tW) / 2.0)
        dY = int(max(0, 28 - tH) / 2.0)

        padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                                    left=dX, right=dX,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))
        padded = cv2.resize(padded, (28, 28))

        padded = padded.astype("float32") / 255.0
        padded = np.expand_dims(padded, axis=-1)
        chars.append(padded)
    return chars


def get_recognized_character(segment):
    segment = CharRecogModel.get_transform()(segment).unsqueeze(0)
    segment = segment.to(device)
    logits = char_recog_model(segment)  # Shape of logits is (1, N_CLASSES)
    return class_list[logits.argmax().cpu().item()]


def recognize_image(img, funcs):
    segments = get_character_segments(img, funcs)
    characters = []
    for segment in segments:
        characters.append(get_recognized_character(segment))
    return ''.join(characters)


def test_image():
    for k, v in sample_dataset.items():
        sample_dataset[k] = (v[0], cv2.imread(k))

    best = {
        'funcs': [],
        'score': -1
    }
    for n_funcs in range(len(all_funcs)+1):
        for funcs_idx, funcs in enumerate(
            itertools.permutations(all_funcs, n_funcs)
        ):
            correct = 0
            for sample in sample_dataset.values():
                if recognize_image(sample[1], funcs) == sample[0]:
                    correct += 1
            if correct > best['score']:
                best['funcs'] = [funcs]
                best['score'] = correct
            elif correct == best['score']:
                best['funcs'].append(funcs)
            print(f'n_funcs={n_funcs:<10} \
                    func_idx={funcs_idx:<10} \
                    correct={correct}')

    if best['score'] > 0:
        print(f'\n\nBest score is {best["score"]}/{len(sample_dataset.keys())}:- \
                \n{best["funcs"]}')
    else:
        print('\n\nNo permutation achieved a positive score')


if __name__ == '__main__':
    test_image()
