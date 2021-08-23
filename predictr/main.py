import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_model, predict

# defining the main app
app = FastAPI(title="predictr", docs_url="/")
app.add_event_handler("startup", load_model)

# class which is expected in the payload
class QueryIn(BaseModel):
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


# class which is returned in the response
class QueryOut(BaseModel):
    loan: str


# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}


@app.post("/predict_cred_scoring", response_model=QueryOut, status_code=200)
# Route to do the prediction using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the flower_class predicted (200)
def predict_flower(query_data: QueryIn):
    output = {"loan": predict(query_data)}
    return output


@app.post("/reload_model", status_code=200)
# Route to reload the model from file
def reload_model():
    load_model()
    output = {"detail": "Model successfully loaded"}
    return output


# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
