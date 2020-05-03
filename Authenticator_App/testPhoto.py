#from facenet_pytorch import InceptionResnetV1
from preProcessPhoto import preProcessPhoto
from endpoint import endpointConnection
import argparse

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("file_path", help="Directory file of the image preprocess", type=str)
parser.add_argument("keys", help="File with the keys to connect to SageMaker", type=str)

#MODEL = InceptionResnetV1(pretrained='vggface2').eval()

def testPhoto(file_path, keys , model):
    embedding = preProcessPhoto(file_path, model)
    post_return = endpointConnection(embedding['data'], keys)
    print(post_return)
    return post_return


def main():
    args = parser.parse_args()
    testPhoto(args.file_path,args.keys, MODEL)


if __name__ == "__main__":
    main()
