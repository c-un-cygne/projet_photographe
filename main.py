from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask("Focal")
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key')  # Nécessaire pour session et flash

bcrypt = Bcrypt(app)

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
            'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
            'role': 'user'
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
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            return render_template('login.html', erreur="Mot de passe incorrect.")
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = db['users'].find_one({'username': session['user']}, {'password': 0})
    post_count = db['photos'].count_documents({'user': session['user']})
    return render_template('profile.html', user=user, post_count=post_count, follower_count=0, following_count=0)

@app.route('/disconnect')
def disconnect():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/publish', methods = ["POST","GET"])
def publish():
    if 'user' not in session:
        return render_template('register.html')
    if request.method == "POST":
        db_photos = db["photos"]
        if request.form['title'] and request.form['image']:
            db_photos.insert_one({
                'photo':request.form['image'],
                'description':request.form['description'],
                'title':request.form['title'],
                'user': session['user'],
                'location_lat': request.form['location_lat'],
                'location_long': request.form['location_long'],
                'type': request.form['type'],
            })
        return redirect(url_for('index'))
    else:
        return render_template('publish.html', erreur = "Fill in all the mandatory fields")

@app.route('/search')
def search():
    query = request.args.get('q','').strip()
    if query=='':
        res = list(db['photos'].find({}))
    else:
        res = list(db['photos'].find({
            "$or":[
                {"title" : {"$regex":query,"$options":"i"}},
                {"type":{"$regex":query,"$options":"i"}}
            ]
        }))
    return render_template("search_result.html", photos=res[::-1], query=query)

@app.route('/index/<id_photo>')
def article_open(id_photo):
    res = db['photos'].find_one({'_id':ObjectId(id_photo)})
    return render_template('article_open.html', photo = res)

app.run(host='0.0.0.0', port=81)