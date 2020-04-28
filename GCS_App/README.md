virtualenv .myenv
source .myenv/bin/activate
make
export FLASK_APP=main.py



Deploy to GCR   
```bash
gcloud builds submit --tag gcr.io/cropthisface/recognizer
```
Once is deployed go to Google Cloud Run, create a service and select the Container that we just create. After this go to settings and select the desired configuration.
In our case we applied the following configuration:
![Conf. Details](https://user-images.githubusercontent.com/43391630/80400504-e4932600-8888-11ea-84e9-9a701ac430e8.png)

If you do some modifications to the project you would need to re run the previous steps.

Service name (recognizer):  recognizer <br>
Please specify a region:  [7] us-east1  <br>
The image can be found on [gcr.io/cropthisface/recognizer](https://gcr.io/cropthisface/recognizer)  <br>