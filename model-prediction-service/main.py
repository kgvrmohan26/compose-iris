from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from  ml_utils import predict

app = Flask(__name__)


@app.route('/', methods=['GET'])
def my_form():
    return render_template('Capstone.html')


@app.route('/', methods=['GET','POST'])
def my_form_post():
    url = request.form['url']
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    #print("Title of the website is : ")
    #title=soup.title.get_text()
    description = soup.title.get_text()
    for p in soup.find_all('p'):
        if len(description) <= 1500:
            description = " ".join([description, p.get_text()])
    category=predict (description)
    print (category)
    return render_template('Capstone.html', result = category.upper())


if __name__ == "__main__":
    app.run()
