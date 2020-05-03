import argparse
import boto3
import boto.s3.connection
import sys
import json

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("video_file", help="Directory file of the video",type=str)
parser.add_argument("bucket_name", help="Name of the bucket to upload to", type = str)
parser.add_argument("person_name", help="Name of the person in the video",type=str)
parser.add_argument("--keys", help="file with access keys", type = str) # None is default 


def uploadBucket(video_file, bucket_name, person_name, keys = None):
    """Upload a video to an S3 bucket.
    The bucket could be an external bucket only if the keys are provided

    :param video_file: Video file to upload
    :param bucket_name: Bucket to upload to
    :param person_name: S3 object name.
    :return: String 
    """
    if keys is None:
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(video_file, bucket_name, person_name)
            print(f'{video_file} has been uploaded correctly to: {bucket_name}/{person_name}')
        except: # catch all
            print(sys.exc_info()[0])
    
    else:
        # Read keys.json if selected
        with open(keys) as k:
            keys = json.load(k)
        #we need to solve the problem to connect to the bucket'
        s3_client = boto3.client('s3', 
                      aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                      aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                      region_name = keys["REGION_NAME"]
                      )
        try:
            response = s3_client.upload_file(video_file, bucket_name, person_name)
            print(f'{video_file} has been uploaded correctly to: {bucket_name}/{person_name}')
        except: # catch all
            print(sys.exc_info()[0])


def main():
  args = parser.parse_args()
  uploadBucket(args.video_file,args.bucket_name,args.person_name,args.keys)

if __name__ == "__main__":
    main()
