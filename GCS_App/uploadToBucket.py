import argparse
import boto3
import sys
import json

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("file", help="Directory file of the video", type=str)
parser.add_argument("bucket_name", help="Name of the bucket to upload to", type=str)
parser.add_argument("--key", help="Name and path where the file will be uploaded", type=str)
parser.add_argument("--credentials", help="file with access credentials", default='A_keys.json', type=str)  # None is default


def uploadToBucket(file, bucket_name, key=None, credentials='A_keys.json'):
    """Upload a file into a bucket
    The bucket could be an external bucket only if the keys are provided

    :param video_file: Video file to upload
    :param bucket_name: Bucket to upload to
    :param person_name: S3 object name.
    :return: String 
    """
    if key is None:
        key = file
    with open(credentials) as k:
        credentials = json.load(k)
    # Connect with S3
    s3_client = boto3.client('s3',
                    aws_access_key_id = credentials["AWS_ACCESS_KEY_ID"], 
                    aws_secret_access_key = credentials["AWS_SECRET_ACCESS_KEY"], 
                    region_name = credentials["REGION_NAME"]
                )
    try:
        s3_client.upload_file(file, bucket_name, key)
        print(f'{file} has been uploaded correctly to: {bucket_name}/{key}')
    except:
        # Catch all
        print(sys.exc_info()[0])


def main():
    args = parser.parse_args()
    uploadToBucket(args.file, args.bucket_name, args.key, args.credentials)


if __name__ == "__main__":
    main()