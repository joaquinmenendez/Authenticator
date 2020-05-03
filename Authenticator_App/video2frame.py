import argparse
import cv2
import os

parser = argparse.ArgumentParser()
parser.add_argument("video_file", help="Directory file of the video",type=str)
parser.add_argument("name", help="Name of the person that appear on the video", type = str)
parser.add_argument("--mod_num", help="Save frames each mod_num of time", default = 5, type = int)
parser.add_argument("--output_file", help="Directory for saving the frames",type=str) # None is default 
parser.add_argument("--rotate", help="[ROTATE_90_CLOCKWISE, ROTATE_180, ROTATE_90_COUNTERCLOCKWISE]", default ='ROTATE_90_CLOCKWISE', type = str) 


def video2frame(video_file, person_name, mod_num=5, output_file=None, rotate='ROTATE_90_CLOCKWISE'):
    """
    This function converts video to frames and it stores it in a directory

    Args:
    video_file (str): Directory file of the video
    name (str): Name of the person in the video
    mod_num (int): Save frames each mod_num of time
    output_file (str): Directory for saving the frames locally

    Returns:

    """
    video = cv2.VideoCapture(video_file)
    video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = frame_list(video, video_len, mod_num)
    assert person_name is not None, "Name not found. Please insert a person name"
    if output_file is not None:
        # Saving images in output_file dir.
        # CV2 does not identify if the camera used was frontal or backward.
        # We are using only frontal camera so we are rotating the frames
        if rotate == None:
            [cv2.imwrite(os.path.join(output_file, '{name}_{num}.jpg'.format(name=person_name, num=str(i))),
         frame) for i, frame in enumerate(frames, 1)]
        else:
            [cv2.imwrite(os.path.join(output_file, '{name}_{num}.jpg'.format(name=person_name, num=str(i))),
            cv2.rotate(frame, eval("cv2." + rotate))) for i, frame in enumerate(frames, 1)]
        print("{0} images saved in {1}".format(len(frames), output_file))
    else:
        [cv2.imwrite(os.path.join(os.getwd(), '{name}_{num}.jpg'.format(name=person_name, num=str(i))),
         cv2.rotate(frame, eval("cv2." + rotate))) for i, frame in enumerate(frames, 1)]
        print("{0} images saved in {1}".format(len(frames), output_file))


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
    video2frame(args.video_file, args.name, args.mod_num, args.output_file, args.rotate)


if __name__ == "__main__":
    main()
