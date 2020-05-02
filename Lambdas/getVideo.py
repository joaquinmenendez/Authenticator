#This is the code of the labda function
# Technical details:
## Memory 320 MB
## Runtime 1 minute
## Layers: arn:aws:lambda:us-east-1:177627986553:layer:cv2-boto3:1

#### Description
# Author: Joaquin Menendez
# This Lambda function takes a video from a bucket in AWS ,
# extract N images per second from the video and upload it to a bucket that the user can select.
import boto3
import os
import pickle
import io
import cv2
import shutil


def lambda_handler(event,context):
	# TODO implement
	event = dict(event)
	get_video(event)
	return {"Status" : "Success"}



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
    video = cv2.VideoCapture(video_path)
    video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = frame_list(video, video_len, mod_num)
    # Iterate over frames and store every frame a an individual object
    try:
    	shutil.rmtree('/tmp/frames')
    except:
    	os.mkdir('/tmp/frames')
    print('directory made') 
    [cv2.imwrite(os.path.join('/tmp/frames','{name}_{num}.jpg'.format(name=person_name, num=str(i))), cv2.rotate(frame, eval("cv2." + rotate) ))
    for i,frame in enumerate(frames,1)] 
    print("{0} images saved in temp/frames/{1}".format(len(frames),person_name))
    len_files = len(os.listdir('/tmp/frames/')) #how many files
    print(f'Uploading {len_files} files to {bucket_name}/{person_name}/Frames')
    print(os.listdir('/tmp/frames/'))
    for file in os.listdir('/tmp/frames'):
    	key = f'{person_name}/frames/{file}'
    	s3_client.upload_file(os.path.join('/tmp/frames',file), bucket_name, key) 
    print ('Done!')
    shutil.rmtree('/tmp/frames')


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
