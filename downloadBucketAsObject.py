## Connect to S3 Bucket
import argparse
import boto3
import boto.s3.connection
import sys
import json
import os

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("bucket_name", help="Name of the bucket to download from", type = str)
parser.add_argument("file_name", help="Name of the video inside the bucket",type=str)
parser.add_argument("output_file", help="Directory to store the video",type=str)
parser.add_argument("--keys", help="File with access keys") # None is default 
parser.add_argument("--name", help='Name of the person')

def downloadBucket(bucket_name, file_name, output_file, keys = None, name = None):
    """Download an object from a S3 Bucket.
    The bucket could be an external bucket only if the keys are passed.
    
    Args:
       bucket_name (str): Name of the bucket to download from
       file_name (str): The name of the key to download from
       output_file (str): The path to the file to download to.
       keys (json): Json with credential keys
    

    Returns:
       Print statement
    """
    if keys is None:
        s3_client = boto3.client('s3')
        try:
            with open(os.path.join(output_file,name), 'wb') as f:
                s3_client.download_fileobj(bucket_name, file_name, f)
            print(f'{file_name} has been downloaded correctly to: {os.path.join(output_file,name)}')
        except: # catch all
            print(sys.exc_info()[0])
    
    else:
        #read keys.json files
        with open(keys) as k:
            keys = json.load(k) 
       
        #we need to solve the problem to connect to the bucket'
        s3_client = boto3.client('s3', 
                      aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                      aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                      region_name = keys["REGION_NAME"]
                      )
        try:
            with open(os.path.join(output_file,name), 'wb') as f:
                s3_client.download_fileobj(bucket_name, file_name, f)
            print(f'{file_name} has been downloaded correctly to: {os.path.join(output_file,name)}')
        except: # catch all
            print(sys.exc_info()[0])


def main():
  args = parser.parse_args()
  downloadBucket(args.bucket_name,args.file_name,args.output_file,args.keys, args.name)

if __name__ == "__main__":
    main()