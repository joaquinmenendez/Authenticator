import argparse
import cv2
from PIL import Image
import os

parser = argparse.ArgumentParser()
parser.add_argument("video_file", help="Directory file of the video",type=str, )
parser.add_argument("output_file", help="Directory for saving the frames",type=str)
parser.add_argument("fig_name", help="Name of the image to be saved", type = str)
parser.add_argument("--mod_num", help="Save frames each mod_num of time", default = 5, type = int)

def video2frame(video_file,output_file,fig_name,mod_num ):
  """
  This function converts video to frames and saves it into the 

  Args:
    video_file (str): Directory file of the video
    output_file (str): Directory for saving the frames
    mod_num (int): Save frames each mod_num of time
    fig_name (str): Name of the image to be saved

  Returns:
    Print statement
  """
  video = cv2.VideoCapture(video_file)
  video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  frames = frame_list(video, video_len, mod_num)

  # Saving images in output_file dir
  [cv2.imwrite(os.path.join(output_file,'{name}_{num}.jpg'.format(name=fig_name,num=str(i))), cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
  for i,frame in enumerate(frames,1)]
  
  return print("{0} images saved in {1}".format(len(frames),output_file))

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
  video2frame(args.video_file,args.output_file,args.fig_name,args.mod_num)

if __name__ == "__main__":
    main()

