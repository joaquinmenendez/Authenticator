import os
import argparse
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import re
import torchvision.transforms as transforms

parser = argparse.ArgumentParser() # Parser for command-line options
parser.add_argument("file", help="Directory with the users and cropped images",type=str)
parser.add_argument("--tensor", help="Returns embeddings as tensor, instead of numpy arrays",type=bool)

def readFaces(file,model,tensor = False):
    """
    Reads all images from a file and returns all the embedings with their corresponding label
    
				Args:
       file (str): Name of the directory that contains all images 
       model (object): Model to do embeddings
       tensor (bool): Returns embeddings as tensor, instead of numpy arrays
   
    Returns:
       train (list): List of embbedings
       test (list): List of labels
				
    """
    face_dict = {}
    for roots,dirs,files in os.walk(file):
        emb_list = []
        for file in files:
            if '.jpg' in file:
                print(file)
                path = os.path.join(roots,file)
                img_emb = embeddings(path,model)
                if not tensor:
                    img_emb = img_emb.detach().numpy()
                    emb_list.append(img_emb)
        face_dict[re.sub("_.*$","",file)] = emb_list
    train, label = [], []
    for key, values in face_dict.items():
        for val in values:
            train.append(val)
            label.append(key)
    return train, label
        

def embeddings(file, model):
    """
    Creates an embedding of the image in the file
    
				Args:
       file (str): Directory of the image
       model (object): Model to do embeddings
       tensor (bool): Returns embeddings as tensor, instead of numpy arrays
    

    Returns:
    			embeddings (obj): Returns the embedding of the image in a numpy array or tensor 
	
    """
    img = Image.open(file).convert('RGB')
    img_tensor = transforms.functional.to_tensor(img)
    embedding = model(img_tensor.unsqueeze(0))[0]
    return embedding
    
def main():
				resnet = InceptionResnetV1(pretrained='vggface2').eval()
				args = parser.parse_args()
				readFaces(args.file, resnet, args.tensor)

if __name__ == "__main__":
    main()