import argparse
import cv2
from PIL import Image
import pickle
from uploadBucketAsObject import uploadBucketAsObject
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("video_file", help="Directory file of the video",type=str)
parser.add_argument("--mod_num", help="Save frames each mod_num of time", default = 5, type = int)
parser.add_argument("--name", help="Name of the person that appear on the video", type = str)
parser.add_argument("--output_file", help="Directory for saving the frames",type=str) # None is default 
parser.add_argument("--bucket_keys", help="file with access keys", type = str) # None is default 
parser.add_argument("--rotate", help="[ROTATE_90_CLOCKWISE, ROTATE_180, ROTATE_90_COUNTERCLOCKWISE]", default ='ROTATE_90_CLOCKWISE', type = str) 

def video2frame(video_file, mod_num, person_name = None, output_file = None, bucket_keys = None, rotate = 'ROTATE_90_CLOCKWISE' ):
  """
  This function converts video to frames. It has the option to save the frames as images
  in a local directory and/or into a s3 bucket.a
  If the user want to store the images into a bucket it should pass the arg `bucket_keys`. 

  Args:
    video_file (str): Directory file of the video
    mod_num (int): Save frames each mod_num of time
    output_file (str): Directory for saving the frames locally
    bucket_keys (str): Path to a json file containing  a bucket's credentials.
  Returns:
    frames (list): List of numpy arrays representing each frame
  """
  video = cv2.VideoCapture(video_file)
  video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  frames = frame_list(video, video_len, mod_num)
  if person_name is None:
    person_name = input('Please write the name of the person that appears in this video: ')
  if output_file is not None:
    # Saving images in output_file dir.
    # CV2 does not identify if the camera used was frontal or backward.
    # We are using only frontal camera so we are rotating the frames
    [cv2.imwrite(os.path.join(output_file,'{name}_{num}.jpg'.format(name=person_name, num=str(i))), cv2.rotate(frame, eval("cv2." + rotate) )) 
    for i,frame in enumerate(frames,1)]
    print("{0} images saved in {1}".format(len(frames),output_file))
  #I f the user pass the argumen bucket_keys  
  if bucket_keys is not None:
    with open(bucket_keys) as k:
      keys = json.load(k)
    bucket_name = keys["BUCKET_NAME"]
    # Iterate over frames and store every frame a an individual object
    for n,frame in enumerate(frames):
      p_name =  f"{person_name}/{person_name}_{n}.pickle" #it's saving as an object every frame
      uploadBucketAsObject(video_file, frame, bucket_name, p_name, keys = bucket_keys)

def frame_list(video, video_len, mod_num):
  """
  Receives a video capture from cv2 and the video length, 
  it returns a list of frames

  Args:
    video (np.array): A video converted to numpy array
    video_len (int): Number of frames in the video
    mod_num (int): Save frames each mod_num of time

  Returns:
    frames (list): List of numpy arrays representing each frame
  """
  frames = []
  for i in range(video_len):
    # Load frame
    success = video.grab()
    if i % mod_num == 0:
        success, frame = video.retrieve()
    else:
        continue
    if not success:
        continue
    # Add to batch
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frames.append(frame)
  return frames

def main():
  args = parser.parse_args()
  video2frame(args.video_file,args.mod_num, args.name, args.output_file,args.bucket_keys, args.rotate)

if __name__ == "__main__":
    main()

