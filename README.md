# Authenticator App
### Authors:
- [Azucena Morales](https://github.com/AzucenaMV)
- [Joaquin Menendez](https://github.com/joaquinmenendez)
- [Julia Oblasova](https://github.com/IuliiaO)

A facial recognition pipeline that employs a Flask App running on Google Cloud Run to upload and preprocess videos of people faces. The processed data is uploaded to AWS Sagemaker where a SVM model is trained and deployed. The user could interact with this ML model using the Flask app or sending a POST request.<br>
You can see a quick demostration [here.](https://youtu.be/1SOxggxeDqo)

**Keywords**: *GCR, Flask, Container, SageMaker, Pytorch, Scikit-Learn*


Authenticator App is a cloud-based application that recognizes team members and assigns appropriate rights of access (or identifies an unauthorized attempt and declines the access).

The app process is described below:

1). A team lead uploads videos of each team member along with the names and access rights: for example, Julia Oblasova – data science manager. All videos are upload to the Flask App.

2). The app splits each video into single frames using python library CV. Each n frame is saved.

3) For each frame, face detection is done using a Multi-Task Cascaded Convolutional Neural Network (MTCNN). If the model detects a face, the cropped and scaled image with the face will be used to train the model. 

4). The collection of cropped images with faces is converted to embeddings using a VGG-16 net model that has been pretrained in faces. Steps 2). 3). and 4) are completed in GCR.

5). The result of preprocessing step is a pickle object with a dictionary of image embeddings and labels. 

6). Using Sagemaker an SVM model is trained using the using the pickle object that is allocated in an S3 bucket.

7). After the training process is completed, Sagemaker deploys the model to an ednpoint.

8). For the testing step, a user submits a photo. The photo is preprocessed with steps 3) and 4) in GCR. Then, the embedding is passed as a binary file in numpy format through an endpoint to the Sagemaker SVM model. Finally, the model predicts who is in the photo. If the probability of recognition is 90% or above, a user on a photo will be granted the access rights.

Note: a user may connect to SageMaker directly through the console via a POST request.

## To run this app locally

1)  Clone this repository.<br>
2)  Create a virtual environment<br>
```bash
virtualenv .myenv
source .myenv/bin/activate
make install
```
3) Run it
```python
python3 main.py
```


## Flask App in Google Cloud Run

We need to create an image for our container using our `Dockerfile`
```Dockerfile
#From Image selected
FROM python:3.7.3-stretch

# Working Directory

WORKDIR /authentificator

# Copy source code to working directory

COPY . main.py /authentificator/

# Install packages from requirements.txt

RUN pip install --upgrade pip &&\
    pip install torch --no-cache-dir torch &&\
	pip install facenet_pytorch --no-cache-dir  &&\
    pip install -r requirements.txt

#Espose a port

EXPOSE 8080

CMD ["python", "main.py"]
```
Deploy to GCR   
```bash
gcloud builds submit --tag gcr.io/cropthisface/authentificator
```
After the image is deployed we create a new service. <br>
Select the container registry image
![image1](https://user-images.githubusercontent.com/43391630/80896397-7781f500-8cbb-11ea-954a-c1eb47e961c4.png) <br>
Set the following settings
![image2](https://user-images.githubusercontent.com/43391630/80851250-88b10000-8bee-11ea-9b1a-9506ec25add7.png)


## Sagemaker

We used our own personal AWS account for this project. 
In case that you wanted to replicate this project create a Sagemaker session and write the **access** and **secret** keys into a json file like this:

```json
{
"AWS_ACCESS_KEY_ID": "",
"AWS_SECRET_ACCESS_KEY": "",
"REGION_NAME": "",
"ROLE":"example:  arn:aws:iam::706015522303:role/sagemaker-role",
"ENDPOINT_NAME" : "",
"BUCKET_NAME": ""
}
```
The data should be stored in `tmp/keys/sagemaker`.
The Flask app is calling the function `train_deploy_model.py ` which is going to send to sagemaker the model we want to train. In this case we train a SVM located in `tmp/model.py`. 

