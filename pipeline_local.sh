#!/bin/bash

echo Processing {$1}:
echo Keys file: {$2}

python3 video2frame.py videos/$1.* --output_file images/$1 --name $1 #--bucket_keys $2
python3 cropAllFaces.py images/$1 cropped_images/$1 
#python3 cropAllFaces.py images/$1 iuliia-bucket --keys $2