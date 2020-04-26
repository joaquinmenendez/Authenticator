import argparse
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import torchvision.transforms as transforms
import json

parser = argparse.ArgumentParser()  # Parser for command-line options
parser.add_argument("file", help="Directory with the users and cropped images", type=str)
parser.add_argument("--tensor", help="Returns embeddings as tensor, instead of numpy arrays", type=bool)


def embeddings(file, tensor=False):
    """
    Creates an embedding of the image in the file
    Args:
        file (str): Directory of the image

    Returns:
        embeddings (obj): Returns the embedding of the image in a numpy array or tensor 

    """
    model = InceptionResnetV1(pretrained='vggface2').eval()
    img = Image.open(file).convert('RGB')
    img_tensor = transforms.functional.to_tensor(img)
    embedding = model(img_tensor.unsqueeze(0))[0]
    if not tensor:
        embedding = embedding.detach().numpy()
    dic = {}
    dic["data"] = embedding.astype(float).tolist()
    j_embedding = json.dumps(dic)
    print (j_embedding)
    return j_embedding


def main():
    args = parser.parse_args()
    return embeddings(args.file, args.tensor)


if __name__ == "__main__":
    main()