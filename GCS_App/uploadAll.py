import argparse
import boto3
import os
import json


parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("path", help="Directory where the files are located", type=str)
parser.add_argument("upload_location", help="The new path where the files are being upload", type=str)
parser.add_argument("keys", help="file with access keys", type=str)


def uploadAll(path, upload_location, keys):
    with open(keys) as k:
        keys = json.load(k)
    s3_client = boto3.client('s3', 
                        aws_access_key_id = keys["AWS_ACCESS_KEY_ID"], 
                        aws_secret_access_key = keys["AWS_SECRET_ACCESS_KEY"], 
                        region_name = keys["REGION_NAME"]
                        )
    len_files = len(os.listdir(path))
    print(f'Uploading {len_files} files to {upload_location}')
    for file in os.listdir(path):
        key = upload_location + '/' + file
        s3_client.upload_file(os.path.join(path, file), keys["BUCKET_NAME"], key)
    print ('Finished uploading files!')


def main():
    args = parser.parse_args()
    uploadAll(args.path, args.upload_location, args.keys)


if __name__ == "__main__":
    main()