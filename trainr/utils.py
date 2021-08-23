import os
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pandas import read_csv

# define the class encodings and reverse encodings
classes = {0: "Bad", 1: "Good"}
r_classes = {y: x for x, y in classes.items()}
global pipe

# function to train and load the model during startup
def init_model():
    if not os.path.isfile("models/CredScore.pkl"):
            #Load data set from https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data
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


# function to train and save the model as part of the feedback loop
def train_model(data):
    # load the model
    clf = pickle.load(open("models/CredScore.pkl", "rb"))

    # pull out the relevant X and y from the FeedbackIn object
    X = [list(d.dict().values())[:-1] for d in data]
    y = [r_classes[d.loan] for d in data]

    # fit the classifier again based on the new data obtained
    #clf.fit(X, y)
    #lobal pipe
   #pipe.fit(X,y)

    # save the model
    pickle.dump(clf, open("models/CredScore.pkl", "wb"))
