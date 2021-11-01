from pyspark.ml.classification import NaiveBayes
import numpy as np
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql.types import StringType

global model
global spark

spark = SparkSession.builder.master("local[1]").appName('prediction').getOrCreate()
model = PipelineModel.load("../models")

def predict(description):
    classes = {0: 'cryptocurrency', 1: 'Finance', 2: 'Sports', 3: 'Environment', 4: 'Business', 5: 'Health',
              6: 'Politics', 7: 'Crime', 8: 'Education', 9: 'Religion',10: 'Entertainment'}
    ex1 = spark.createDataFrame([(description, StringType())], ["description"])
    category = model.transform(ex1)#-------------------
    result=category.select("prediction").collect()[0][0]
    print (classes[result])
    return classes[result]

#load_model()
#predict("Trump will win elections")


