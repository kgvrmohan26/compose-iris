from kafka import KafkaConsumer
import json
from pymongo import MongoClient

consumer = KafkaConsumer('news', bootstrap_servers=['localhost:9092'])
client = MongoClient("mongodb+srv://Capstone:Capstone@capstone.itrtq.mongodb.net/Capstone?retryWrites=true&w=majority")
mydb = client["Capstone"]
mycoll = mydb["news"]


for message in consumer:
    record = json.loads(message.value)
    news_record=json.loads(record)
    mycoll.insert_one(news_record)
    print (news_record)

