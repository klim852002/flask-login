from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from flask_mail import Mail, Message
import logging
import string
import random

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'lee.kuoping@gmail.com',
	MAIL_PASSWORD = ''
	)
mail = Mail(app)

app.config['MONGO_DBNAME'] = 'login_assignment'
app.config['MONGO_URI'] = 'mongodb://bruno:oromico@ds123331.mlab.com:23331/login_assignment'

mongo = PyMongo(app)

# @app.route('/add')
# def add():
#     user = mongo.db.users
#     user.insert({'name' : 'Davide'})
#     return 'Added user!'

@app.route('/')
def index():
    if 'username' in session:
        return 'you are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        # compares the hashed user input password against the database hashed password
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    # if login_user is null
    return 'Invalid username/password combination'


@app.route('/account')
def account():
    return render_template('account.html')

# @app.route('/send', methods=['POST', 'GET'])
# def send_mail():
# 	try:
# 		msg = Message("Send Mail Tutorial!",
# 		  sender="lee.kuoping@gmail.com",
# 		  recipients=[request.form['username']])
# 		msg.body = "Please login with the following password" + "123abc"
# 		mail.send(msg)
# 		return redirect(url_for('account'))
# 	except Exception, e:
# 		return(str(e))


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        generated_pw = id_generator()

        if existing_user is None:
# hashpass from a randomly generated password
# send the generated password to new user
            hashpass = bcrypt.hashpw(generated_pw.encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
        try:
    		msg = Message("Send Mail Tutorial!",
    		  sender="lee.kuoping@gmail.com",
    		  recipients=[request.form['username']])
    		msg.body = "Please login with the following password" + generated_pw
    		mail.send(msg)
    		return redirect(url_for('account'))
    	except Exception, e:
    		return(str(e))
            # session['username'] = request.form['username']
# after registration redirects to index
            # return redirect(url_for('send_mail'))
# if post action and existing_user
        return 'That username already exists!'
# if using get method
    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
