from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, split, udf, trim, concat
import pyspark.ml.feature
from pyspark.ml.feature import Tokenizer,StopWordsRemover,CountVectorizer,IDF,RegexTokenizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, NaiveBayes
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.types import StringType
from pyspark import SparkContext
import pickle
import numpy as np
import joblib
from pyspark.ml import Pipeline, PipelineModel


my_spark1 = SparkSession \
    .builder \
    .appName("myApp1") \
    .config("spark.mongodb.input.uri",
            "mongodb+srv://Capstone:Capstone@capstone.itrtq.mongodb.net/Capstone.news") \
    .config("spark.mongodb.output.uri",
            "mongodb+srv://Capstone:Capstone@capstone.itrtq.mongodb.net/Capstone.news") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
    .getOrCreate()


def load_model():
    df = my_spark1.read.format("mongo").load()
    df = df.drop('_id')
    df = df.drop('date')
    df = df.drop('source')
    df = df.select((concat(col("summary"), col("title")).alias("description")), col("category").alias("category"))
    df = df.na.drop()
    # df.groupBy("category").count().show()
    df.groupBy("category") \
        .count() \
        .orderBy(col("count").desc()) \
        .show()
    # regular expression tokenizer
    regexTokenizer = RegexTokenizer(inputCol="description", outputCol="words", pattern="\\W")
    # stop words
    add_stopwords = ["http", "https", "amp", "rt", "t", "c", "the"]
    stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)
    # bag of words count
    countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

    from pyspark.ml import Pipeline
    from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
    label_stringIdx = StringIndexer(inputCol="category", outputCol="label")


    (trainingData, testData) = df.randomSplit([0.7, 0.3], seed = 100)
    print("Training Dataset Count: " + str(trainingData.count()))
    print("Test Dataset Count: " + str(testData.count()))

    #Naive Bayes
    nb = NaiveBayes(smoothing=1)
    pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx,nb])
    global model
    model = pipeline.fit(trainingData)
    predictions = model.transform(testData)
    predictions.filter(predictions['prediction'] == 0) \
        .select("description", "category", "probability", "label", "prediction") \
        .orderBy("probability", ascending=False) \
        .show(n=10, truncate=30)
    dataFrame =predictions.dropDuplicates(["category"])
    dataFrame.show(20)

    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    evaluator.evaluate(predictions)
    accuracy = evaluator.evaluate(predictions)
    print("Model accuracy", accuracy)
    model.write().overwrite().save("../models")



# function to predict the flower using the model
def predict(query_data):
    classes = {0: 'cryptocurrency', 1: 'Finance', 2: 'Sports', 3: 'Environment', 4: 'Business', 5: 'Health',
              6: 'Politics', 7: 'Crime', 8: 'Education', 9: 'Religion',10: 'Entertainment'}
    x = list(query_data.dict().values())
    var1 = x[0]
    var2 = x[1]
    news = " ".join([var1, var2])
    ex1 = my_spark1.createDataFrame([(news,StringType())],["description"])
    ex1=ex1.drop('_2')#----------------------
    category = model.transform(ex1)#-------------------
    result=category.select("prediction").collect()[0][0]
    return classes[result]

load_model()