from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template("index.html")

@app.route('/Home', methods=['GET', 'POST'])
def Home():
    return "Hello World!"

@app.route('/Report', methods=['GET', 'POST'])
def Report():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
