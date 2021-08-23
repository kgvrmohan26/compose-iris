import os
import uvicorn
import requests
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from utils import process_data

TRAINR_ENDPOINT = os.getenv("TRAINR_ENDPOINT")

# defining the main app
app = FastAPI(title="processr", docs_url="/")

# class which is expected in the payload while training
class DataIn(BaseModel):
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


# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}


@app.post("/process", status_code=200)
# Route to take in data, process it and send it for training.
def process(data: List[DataIn]):
    processed = process_data(data)
    # send the processed data to trainr for training
    #response = requests.post(f"{TRAINR_ENDPOINT}/train", json=processed)
    return {"detail": "Processing successful"}


# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
