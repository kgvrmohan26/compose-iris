import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pandas import read_csv
import pandas as pd

# define a Gaussain NB classifier
clf = GaussianNB()

# define the class encodings and reverse encodings
#classes = {0: "Iris Setosa", 1: "Iris Versicolour", 2: "Iris Virginica"}
classes = {0: "Bad", 1: "Good"}
r_classes = {y: x for x, y in classes.items()}
global pipe


# function to load the model
def load_model():
    global clf
    clf = pickle.load(open("models/CredScore.pkl", "rb"))
    df=read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data",sep=" ",header=None)
    y=df[20]
    X=df.drop(20,axis=1)
    # select categorical and numerical features
    cat_ix=X.select_dtypes(include=['object','bool']).columns
    ct=ColumnTransformer([('o',OneHotEncoder(),cat_ix)],remainder='passthrough')
    clf = GaussianNB()
    global pipe
    pipe=Pipeline([("ct",ct),("clf",clf)])
    
    #Label encode the target variable to have  the classes 0 and 1 
    y=LabelEncoder().fit_transform(y)
            
    #Do the Split and train the model
    X_train, X_test, y_train, y_test= train_test_split(X ,y,test_size=0.2)
    pipe.fit( X_train,y_train)
    pickle.dump(pipe, open("models/CredScore.pkl", "wb"))
    


# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())
    X=pd.DataFrame([x])
    global pipe
    prediction = pipe.predict(X)[0]
    print(f"Model prediction: {classes[prediction]}")
    #return (classes[prediction])
    return classes[prediction]
