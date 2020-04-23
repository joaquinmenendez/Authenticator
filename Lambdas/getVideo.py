#This is the code of the labda function
# Technical details:
## Memory 320 MB
## Runtime 1 minute
## Layers: arn:aws:lambda:us-east-1:177627986553:layer:cv2-boto3:1

import boto3
import os
import pickle
import io
import cv2

def lambda_handler(event,context):
	# TODO implement
	event = dict(event)
	get_video(event)
	return ''


def get_video(event):
	s3_client = boto3.client('s3', 
							 aws_access_key_id = event["AWS_ACCESS_KEY_ID"], 
							 aws_secret_access_key = event["AWS_SECRET_ACCESS_KEY"], 
							 region_name = event["REGION_NAME"]
							)

	s3_client.download_file(event['BUCKET_NAME'], event["KEY"], f'/tmp/{event["KEY"]}' )
	print('Video dowloaded')
	video_path = f'/tmp/{event["KEY"]}' 
	print(video_path)
	video2frame(s3_client, video_path , event['BUCKET_NAME'], event["PERSON_NAME"],  event["MOD_NUM"],  event["ROTATE"])
	return
	
	
def video2frame(s3_client, video_path , bucket_name, person_name, mod_num, rotate ):
  """
  """
  video = cv2.VideoCapture(video_path)
  video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  frames = frame_list(video, video_len, mod_num)
  # Iterate over frames and store every frame a an individual object
  total_files = len(frames)
  for n,frame in enumerate(frames):
    p_name =  f"{person_name}/{person_name}_{n}.pickle" #it's saving as an object every frame
    my_array_data = io.BytesIO()   #binarize into a binary file
    pickle.dump(frame, my_array_data)
    my_array_data.seek(0)
    s3_client.upload_fileobj(my_array_data, bucket_name, p_name)
    print(f'{p_name} has been succesfully uploaded. {n} of {total_files} remaining')
  print('Done!')
	
def frame_list(video, video_len, mod_num):
	"""
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
  
