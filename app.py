# app.py
import base64
import json
import pickle
from io import BytesIO
from flask import Flask, request, jsonify

import cv2
import imutils
from imutils.contours import sort_contours
import numpy as np
from PIL import Image
import torch

from models import CharRecogModel


app = Flask(__name__)

class_list = None
with open('models/class_list.pkl', 'rb') as class_list_file:
    class_list = pickle.load(class_list_file)

device = 'cpu'
char_recog_path = 'models/char_recog.pt'
char_recog_model = CharRecogModel(len(class_list))
char_recog_model.load_state_dict(torch.load(char_recog_path))
char_recog_model = char_recog_model.to(device)
char_recog_model.eval()


def get_character_segments(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    erode = cv2.erode(gray, np.ones((5, 5), np.uint8), iterations=1)
    cv2.imshow("erode", erode)
    cv2.waitKey(2000)
    thresh2 = cv2.threshold(erode, 0, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow("thresh2", thresh2)
    cv2.waitKey(2000)
    image = cv2.GaussianBlur(erode, (3, 3), 0)
    cv2.imshow("gauss", image)
    cv2.waitKey(2000)
    image = cv2.Canny(image, 30, 150)
    cv2.imshow("canny", image)
    cv2.waitKey(2000)
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]

    chars = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        # if (w >= 5 and w <= 150) and (h >= 50 and h <= 120):
        roi = erode[y:y + h, x:x + w]
        thresh = cv2.threshold(roi, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        (tH, tW) = thresh.shape
        if tW > tH:
            thresh = imutils.resize(thresh, width=28)
        else:
            thresh = imutils.resize(thresh, height=28)

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
    cv2.imshow("mat", np.expand_dims(segment.cpu().numpy().squeeze(), -1))
    cv2.waitKey(1000)
    logits = char_recog_model(segment)  # Shape of logits is (1, N_CLASSES)
    return class_list[logits.argmax().cpu().item()]


def recognize_image(img):
    segments = get_character_segments(img)
    characters = []
    for segment in segments:
        # cv2.imshow("mat", segment)
        # cv2.waitKey(1000)
        characters.append(get_recognized_character(segment))
    return ''.join(characters)


def test_image():
    img = cv2.imread('test_img_3.jpeg')
    print(recognize_image(img))


@app.route('/recognize', methods=['POST'])
def recognize():
    data = json.loads(request.get_json())
    img = BytesIO(base64.b64decode(data['image']))
    img = np.array(Image.open(img))[:, :, ::-1]

    submitted_answer = recognize_image(img)
    response = {
        "submitted_answer": submitted_answer
    }
    return jsonify(response)


if __name__ == '__main__':
    test_image()
    # app.run(port=5000, debug=True)