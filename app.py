from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
