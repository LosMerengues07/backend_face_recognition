import scipy.misc
import tensorflow as tf
from facenet import detect_face
import cv2
import matplotlib.pyplot as plt
import imageio
import sys,os
from . import models
import warnings

def recognition(image_path):
    warnings.filterwarnings('ignore')
    minsize = 35  # minimum size of face
    threshold = [0.7, 0.9, 0.7]  # three steps's threshold
    factor = 0.9  # scale factor
    gpu_memory_fraction = 1.0

    print ('Creating networks and loading parameters')

    with tf.Graph ().as_default ():
        gpu_options = tf.GPUOptions (per_process_gpu_memory_fraction=gpu_memory_fraction)
        sess = tf.Session (config=tf.ConfigProto (gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default ():
            pnet, rnet, onet = detect_face.create_mtcnn (sess, None)


    img = imageio.imread (image_path)
    bounding_boxes, _ = detect_face.detect_face (img, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]  # 人脸数目
    print ('找到人脸数目为：{}'.format (nrof_faces))

    #print (bounding_boxes)

    crop_faces = []
    for face_position in bounding_boxes:
        face_position = face_position.astype (int)
        #print (face_position[0:4])
        cv2.rectangle (img, (face_position[0], face_position[1]), (face_position[2], face_position[3]), (0, 255, 0), 2)
        if face_position[0] < 0:
            face_position[0] = 0
        if face_position[1] < 0:
            face_position[1] = 0
        if face_position[2] < 0:
            face_position[2] = 0
        if face_position[3] < 0:
            face_position[3] = 0
        crop = img[face_position[1]:face_position[3],
               face_position[0]:face_position[2], ]
        crop = cv2.resize (crop, (96, 96), interpolation=cv2.INTER_CUBIC)
        crop_faces.append (crop)


    save_path = 'static/img/cook1/'+os.path.basename(image_path)
    plt.imsave(save_path,img)
    return save_path
