virtualenv .myenv
source .myenv/bin/activate
export FLASK_APP=main.py

python3 embeddingFaces.py tmp/Iuliia_6.jpg > somefile