import numpy as np
import cv2
import dlib
import os
from . import models
import matplotlib.pyplot as plt

def heat(filepath):
    detector = dlib.get_frontal_face_detector()
    module_path = os.path.dirname(__file__)
    filename = module_path + '/dat/shape_predictor_68_face_landmarks.dat'
    predictor = dlib.shape_predictor(filename)

    # cv2读取图像
    img = cv2.imread(filepath)

    # 取灰度
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 人脸数rects
    rects = detector(img_gray, 0)
    print("rects:",rects)
    for i in range(len(rects)):
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img,rects[i]).parts()])
        for idx, point in enumerate(landmarks):
            # 68点的坐标
            pos = (point[0, 0], point[0, 1])
            #print(idx,pos)

            # 利用cv2.circle给每个特征点画一个圈，共68个
            cv2.circle(img, pos, 5, color=(0, 255, 0))
            # 利用cv2.putText输出1-68
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(idx+1), pos, font, 0.8, (0, 0, 255), 1,cv2.LINE_AA)


    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2默认为bgr顺序
    save_path = 'static/img/cook2/'+os.path.basename(filepath)
    plt.imsave(save_path,img)
    return save_path