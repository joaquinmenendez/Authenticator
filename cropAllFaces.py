import argparse
import os
import cropFace
import uploadBucket
import cv2
from uploadBucket import uploadBucket
import json


parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("file_directory", help="Name of the directory that contains all images",type=str)
parser.add_argument("output_dir", help="Name of the directory or bucket were the images should be saved",type=str)
parser.add_argument("--keys", help="Json with credential keys", type=str)
 

def cropAll(file_dir, output_dir, keys = None):
    """
    Crop all the functions given a directory and save it locally or in a bucket
    
    Args:
       file_dir (str): Name of the directory that contains all images
       output_dir (str): Name of the directory or bucket were the images should be saved
       keys (json): Json with credential keys
    

    Returns:
       Print statement
    """
     # It creates the folder if it does not exist
    if not keys:
      try:
        os.makedirs(output_dir)
        print("{out} directory created".format(out = output_dir))
      except:
        print("{out} directory exist".format(out = output_dir))


    for file in os.listdir(file_dir):
      img_cropped = cropFace.crop(os.path.join(file_dir,file))
      if img_cropped is not None:
        if not keys:
          print("Saving file {file} in directory {out}".format(file = file, out = output_dir))
          cv2.imwrite(os.path.join(output_dir,file),img_cropped)
        else:
          tmp_file = "tmp_"+file
          tmp_path = os.path.join(os.getcwd(),tmp_file)
          cv2.imwrite(tmp_file, img_cropped) 
          try:
            # Uploading to the bucket
            print("Saving file {file} in bucket {out}".format(file = file, out = output_dir))
            uploadBucket(tmp_path, output_dir, file, keys = keys)
          except: 
            print("error") 
          os.remove(tmp_path)        
    return print("Done!")
  
 
def main():
  args = parser.parse_args()
  cropAll(args.file_directory, args.output_dir, args.keys)

if __name__ == "__main__":
    main()