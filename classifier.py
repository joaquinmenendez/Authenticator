from facenet_pytorch import InceptionResnetV1
#from sklearn.svm import SVC
#from sklearn.metrics import accuracy_score
import os
import argparse
import cv2
import torch
from PIL import Image
import torchvision.transforms as transforms

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("file", help="Directory file of the images", type=str)

def readFaces(file,model):
    face_dict = {}
    for roots,dirs,files in os.walk(file):
        emb_list = []
        for file in files:
            if '.jpg' in file:
                path = os.path.join(roots,file)
                print(path)
                emb_list.append(embeddings(path,model))
        face_dict[file] = emb_list
    return print("Success!")
            

def embeddings(file, model):
    img = Image.open(file).convert('RGB')
    img_tensor = transforms.functional.to_tensor(img)
    #resnet = InceptionResnetV1(pretrained='vggface2').eval()
    embedding = model(img_tensor.unsqueeze(0))
    return embedding
    
# def classifier():
#     model = SVC(kernel='linear', probability=True)
#     model.fit(trainX, trainy)
#     # predict
#     y_train_pred = model.predict(trainX)
#     y_test_pred = model.predict(testX)  

def main():
  args = parser.parse_args()
  resnet = InceptionResnetV1(pretrained='vggface2').eval()
  readFaces(args.file, resnet)
  
if __name__ == "__main__":
    main()