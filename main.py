from flask import Flask, render_template
import pymongo
import os
from dotenv import load_dotenv

app = Flask("Focal")

#conection à la bdd

#initialisation de variable...


@app.route('/')
def index():
    return render_template("index.html")


app.run(host='0.0.0.0',port=81)