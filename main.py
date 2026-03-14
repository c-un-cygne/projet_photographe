from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask("Focal")
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key')  # Nécessaire pour session et flash

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db = client.get_database('Focal')

@app.route('/')
def index():
    photos_data = list(db['photos'].find({}))
    return render_template("index.html",photos=photos_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        db_users = db['users']

        if db_users.find_one({'username': request.form['username']}):
            return render_template('signup.html', erreur="Nom d'utilisateur déjà pris.")
        
        if request.form['password'] != request.form['confirm_password']:
            return render_template('signup.html', erreur="Les mots de passe ne correspondent pas.")
        
        db_users.insert_one({
            'username': request.form['username'],
            'email':request.form['email'],
            'password': request.form['password']
        })
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_users = db['users']

        user = db_users.find_one({'username': request.form['username']})
        if not user:
            return render_template('login.html', erreur="Utilisateur introuvable.")
        if user['password'] != request.form['password']:
            return render_template('login.html', erreur="Mot de passe incorrect.")
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/disconnect')
def disconnect():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/publish', methods = ["POST","GET"])
def publish():
    if 'user' not in session:
        return render_template('register.html')
    if request.method == "POST":
        db_articles = db["photos"]
        if request.form['title'] and request.form['image']:
            db_articles.insert_one({
                'photo':request.form['image'],
                'description':request.form['description'],
                'title':request.form['title'],
                'user': session['user'],
                'location_lat': session['location_lat'],
                'location_long': session['location_long'],
                'type': session['type'],
            })
        return redirect(url_for('index'))
    else:
        return render_template('publish.html', erreur = "Fill in all the mandatory fields")

app.run(host='0.0.0.0', port=81)