import argparse
import boto3
import boto.s3.connection
import sys
import json
import pickle
import io

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("video_file", help="Directory file of the video",type=str)
parser.add_argument("frames", help="Object. Numpy list with frames",type=str) 
#This function was designed to live inside other function. But, if the user has an object he could upload it to the bucket
parser.add_argument("bucket_name", help="Name of the bucket to upload to", type = str)
parser.add_argument("person_name", help="Name of the person in the video",type=str)
parser.add_argument("--keys", help="file with access keys", type = str) # None is default 


def uploadBucketAsObject(video_file, frames, bucket_name, person_name, keys = None):
    '''
    This function uploads a numpy array to an S3 bucket.
    The bucket could be an external bucket only if the keys are provided (--keys)
    
    :param video_file: Video file to upload
    :param: frames: list of numpy arrays composed by frames of `video_file` or a simple element of this list
    :param bucket_name: Bucket to upload to
    :param person_name: The name of the person in the video. The S3 object will be saved with this name
    :param is_object: Boolean. False is default
    :return: None
    '''
    if keys is None:
        s3_client = boto3.client('s3')
        pickle_obj = pickle.dump(frames)
        try:
            response = s3_client.upload_fileobj(fileobj=pickle_obj, bucket=bucket_name, key=person_name)
            print(f'{video_file} has been uploaded correctly to: {bucket_name}/{person_name} as an OBJECT')
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
        uploadObject(s3_client,frames, video_file, bucket_name, person_name)


def uploadObject(s3_client, frames, video_file, bucket_name, person_name):
    '''
    A handler function. It uploads an object to an S3 bucket_name.
    
    :param s3_client: s3_client obj)
    :param frames: list of numpy arrays composed by frames of `video_file`
    :param video_file : string, path to the original video
    :param bucket_name : string
    :param person_name : string
    :return: None
    '''
    #with open(f'{person_name}_binary', 'wb') as file:
    #    pickle.dump(frames, file)
    #binary_obj = pickle.load(open(f'{person_name}_binary', "rb"))
    my_array_data = io.BytesIO()
    pickle.dump(frames, my_array_data)
    my_array_data.seek(0)
    try:
        response = s3_client.upload_fileobj(my_array_data, bucket_name, person_name)
        print(f'{video_file} has been uploaded correctly to: {bucket_name}/{person_name} as an OBJECT')
    except: # catch all
        print('uploadObject error:')
        print(sys.exc_info()[0])
    del (my_array_data)
    


def main():
  args = parser.parse_args()
  uploadBucketAsObject(args.video_file, args.frames,args.bucket_name,args.person_name,args.keys)

if __name__ == "__main__":
    main()
