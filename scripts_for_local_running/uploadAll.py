import argparse
import boto3
import os
import json


parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("path", help="Directory where the files are located",type=str)
parser.add_argument("bucket_name", help="Name of the bucket to upload to", type = str)
parser.add_argument("folder_name", help="The new path where the files are being upload",type=str)
parser.add_argument("--keys", help="file with access keys", type = str) # None is default 



def uploadAll(path, bucket_name, folder_name, keys = None):
	with open(keys) as k:
		keys = json.load(k)
	s3_client = boto3.client('s3', 
                      aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                      aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                      region_name = keys["REGION_NAME"]
                      )
	len_files = len(os.listdir(path))
	print(f'Uploading {len_files} files to {folder_name}')
	for file in os.listdir(path):
		key = folder_name + '/' + file
		s3_client.upload_file(os.path.join(path,file), bucket_name, key)
	print ('Done!')

def main():
  args = parser.parse_args()
  uploadAll(args.path, args.bucket_name, args.folder_name,args.keys)

if __name__ == "__main__":
    main()	