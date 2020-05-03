To run

```bash
virtualenv .myenv
source .myenv/bin/activate
make
```
Deploy to GCR   
```bash
gcloud builds submit --tag gcr.io/cropthisface/recognizer
```
