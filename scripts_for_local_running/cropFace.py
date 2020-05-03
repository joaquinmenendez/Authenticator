import argparse
from facenet_pytorch import MTCNN
import cv2
from matplotlib import pyplot as plt
import numpy as np
from imutils import  url_to_image, opencv2matplotlib


parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("input_img", help="Directory file of the image to crop",type=str)
parser.add_argument("--output", help="[Optional] Directory where the output image be saved to. If selected the numpy output will be override",type=str)

def crop(input_img):
  '''
  :return:  a cropped face in numpy array format
  '''
  img = cv2.imread(input_img)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  mtcnn = MTCNN(select_largest=False, post_process = False, margin = 50)
  img_cropped = mtcnn(img)
  #simple message notifying if a face was detected or not
  if img_cropped is None:
    print(f'Face not detected in file {input_img}')
    return
  img_cropped = img_cropped.permute(1, 2, 0).int().numpy() 
  return img_cropped
  
def plot_crop_face(img_cropped, output_img):
  '''
  :params:
  :return:
  '''
  plt.imshow(img_cropped)  
  plt.axis('off')
  plt.savefig(output_img)

def cropFace(input_img, output_img = None):
  '''
   
  :params:
  :return:
  '''
  if output_img is None:
    return crop(input_img)
    
  else:
    img_cropped = crop(input_img)
    plot_crop_face(img_cropped,output_img)


def main():
  args = parser.parse_args()
  cropFace(args.input_img, args.output)

if __name__ == "__main__":
    main()