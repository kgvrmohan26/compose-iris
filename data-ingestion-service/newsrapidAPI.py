import requests
from kafka import KafkaProducer
import time
import json

def getNews(title):
    url = "https://free-news.p.rapidapi.com/v1/search"
    querystring = {"q": title, "lang": "en", "page": "1", "page_size": "25"}
    headers = {
        'x-rapidapi-key': "3b1d7a3252mshc8b5142455609abp1c8c1ejsn164eebb8369c",
        'x-rapidapi-host': "free-news.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    print (response)
    def json_serializer(newsDist):
        return json.dumps(newsDist).encode("utf-8")
    newsDist = {}
    i=0
    for i in range(len(response['articles'])):
        if (response['articles'][i]['topic']=='news' or 'News' or 'NEWS'):
            category=title
        else:
            category=response['articles'][i]['topic']

        newsDist.update(title=response['articles'][i]['title'], date=response['articles'][i]['published_date'],
                    summary=response['articles'][i]['summary'], category=category,
                    source=response['articles'][i]['link'])
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
        producer.send('news', json.dumps(newsDist))
        i=i+1
        time.sleep(5)
        print (json.dumps(newsDist))

#getNews('Business')