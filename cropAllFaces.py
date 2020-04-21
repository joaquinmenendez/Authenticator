import argparse
import os
import cropFace
import uploadBucket
import cv2
from uploadBucket import uploadBucket
import json


parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("file_directory", help="Directory that contains all images",type=str)
parser.add_argument("output_dir", help="Directory where the output image be saved to, this could also be a bucket",type=str)
parser.add_argument("--keys", help="If isBucket is true keys should be provided",default = None, type=str)


def cropAll(file_dir, output_dir, keys):
  '''
  :return:  a cropped face in numpy array format
  '''
  if not keys:
    for file in os.listdir(file_dir):
      try:
        #print(file)
        img_cropped = cropFace.crop(os.path.join(file_dir,file))
        if img_cropped is not None:
            cv2.imwrite(os.path.join(output_dir,file),img_cropped)
      except: 
        print("Error")
  else:
    # with open(keys) as k:
    #   keys = json.load(k)
    # #   #we need to solve the problem to connect to the bucket'
    # s3_client = boto3.client('s3', 
    #                 aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
    #                 aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
    #                 region_name = keys["REGION_NAME"]
    #                 )
    for file in os.listdir(file_dir):
      img_cropped = cropFace.crop(os.path.join(file_dir,file))
      if img_cropped is not None:
          tmp_file = "tmp_"+file
          tmp_path = os.path.join(os.getcwd(),tmp_file)
          #print(os.getcwd())
          cv2.imwrite(tmp_file, img_cropped)
          try:
              uploadBucket(tmp_path, output_dir, file, keys = keys)
              #s3.put_object(Bucket='mytestbucket',Key='myList001',Body=serializedListObject)
              #response = s3_client.put_object(output_dir, file, key = keys)
              #uploadBucketAsObject(img_cropped,output_dir, file, keys = keys)
              #response = s3_client.upload_fileobj(img_cropped, output_dir, file)
              #s3_client.upload_file(video_file, bucket_name, person_name)
              #print(f'{video_file} has been upploaded correctly to: {bucket_name}/{person_name}')
          except: # catch all
              #print(sys.exc_info()[0])
              print("error")
          #cv2.imwrite(file,img_cropped)
          os.remove(tmp_path)
  return print("Done!")
  
  
 
def main():
  args = parser.parse_args()
  cropAll(args.file_directory, args.output_dir, args.keys)

if __name__ == "__main__":
    main()