from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask("Focal")

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db = client.get_database('Focal')

@app.route('/')
def index():
    photos_data = list(db['photos'].find({}))
    return render_template("index.html",photos=photos_data)


app.run(host='0.0.0.0',port=81)