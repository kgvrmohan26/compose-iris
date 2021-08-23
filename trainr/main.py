import uvicorn
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from utils import init_model, train_model
from typing import List


PREDICTR_ENDPOINT = os.getenv("PREDICTR_ENDPOINT")

# defining the main app
app = FastAPI(title="trainr", docs_url="/")

# calling the load_model during startup.
# this will train the model and keep it loaded for prediction.
app.add_event_handler("startup", init_model)

# class which is expected in the payload while training
class TrainIn(BaseModel):
    p1: str= 'A11'
    p2: int= 6
    p3: str='A34'
    p4: str='A43'
    p5: int=1169
    p6: str='A65'
    p7: str='A75'
    p8: int=4
    p9: str='A93'
    p10: str='A101'
    p11: int=4
    p12: str='A121'
    p13: int=67
    p14: str='A143'
    p15: str='A152'
    p16: int=2
    p17: str='A173'
    p18: int=1
    p19: str='A192'
    p20: str='A201'
    loan:str='Bad'
    
class QueryOut(BaseModel):
    loan: str


# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}


@app.post("/train", status_code=200)
# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and correct flower class
# Response: Dict with detail confirming success (200)
def train(data: List[TrainIn]):
    train_model(data)
    # tell predictr to reload the model
   # response = requests.post(f"{PREDICTR_ENDPOINT}/reload_model")
    return {"detail": "Training successful"}


# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=7777, reload=True)
