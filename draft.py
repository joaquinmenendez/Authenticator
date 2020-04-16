# Libraries
from facenet_pytorch import MTCNN, InceptionResnetV1
import cv2
from pnslib import utils
from PIL import Image
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm
import numpy as np
from imutils import  url_to_image, opencv2matplotlib
#from hof.face_detectors import RfcnResnet101FaceDetector, SSDMobileNetV1FaceDetector,FasterRCNNFaceDetector, YOLOv2FaceDetector, TinyYOLOFaceDetector
import face_recognition


MIN_CONFIDENCE=0.5

def display(img, figsize=(15,15)):
  plt.figure(figsize=figsize)
  plt.axis('off')
  plt.imshow(opencv2matplotlib(img))
  plt.show()


def cropFace(path_to_img)
    img = cv2.imread(path_to_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mtcnn = MTCNN(select_largest=False, post_process = False, margin = 50)
    img_cropped = mtcnn(img)
    plt.imshow(img_cropped.permute(1, 2, 0).int().numpy())
    plt.axis('off')


cropFace("./multimedia/messi.jpg")