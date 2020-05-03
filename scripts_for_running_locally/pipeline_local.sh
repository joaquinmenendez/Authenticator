#!/bin/bash
# 1 : Name 
# 2 : Video file path
# 3 : [ROTATE_90_CLOCKWISE, ROTATE_180, ROTATE_90_COUNTERCLOCKWISE] -- default=ROTATE_90_CLOCKWISE

ROTATE=${3:-ROTATE_90_CLOCKWISE} #set 90 degress as the default rotation (Apple)

echo Processing: $1

#Check if the directory exist. If it does not then create it
if [ -d "$1" ]; then 
    echo A directory for "$1" already exist. 
    echo Adding files...
    ext=$(echo "$2"  | sed 's:.*/::') #I need to extract the symlink. Store everything after the last /
    if [ -f "$1/video/$ext" ]; then #check if ther is a file inside video. If is, then rename
        echo There is a already a video inside this directory with the name $ext
        read -p 'Please select a new name for the this video (dont forget to add the extension): ' new_name
        cp -n $2 $1/video/$new_name #copy the renamed video
    fi
else
    # create directories
    mkdir $1 
    mkdir $1/video && mkdir $1/images && mkdir $1/faces
    ext=$(echo "$2"  | sed 's:.*/::') #I need to extract the symlink. Store everything after the last /
    cp $2 $1/video/$ext #copy the video  from original path with the same name
fi

#Run python scripts
python3 video2frame.py $2 --output_file $1/images --name $1 --rotate $ROTATE # Transform the video into frames
python3 cropAllFaces.py $1/images $1/faces #Crop oly the faces from the images