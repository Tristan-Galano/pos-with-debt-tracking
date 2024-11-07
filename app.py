from flask import Flask, jsonify, render_template,redirect, request, session, url_for

from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


app.secret_key= ['sadsadsadsafgfhjtrew23456uiutjyhg']

import models
app.app_context().push()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():    
    username = request.form["username"]
    password = request.form["password"]
    user = models.User.query.filter_by(username=username).first()
    if username == user.username and password==user.password:
        session['id'] =user.id
        session['username'] = username
        session['admin'] = user.admin
        return redirect('/cashier')
    else:
        return redirect('/')

@app.route("/sign-up")
def create_user():
    if session.get('admin'):
        if session['admin'] == True:
            return render_template("signup.html")
    else:
        return redirect('/cashier')
    
@app.route("/cashier")
def cashier():
      if session.get('username'):
        debtors = models.Debtor.query.all()
        
        return render_template('cashier.html', debtors = debtors)
      else:
          return redirect('/')
      

@app.route('/tansaction', methods=['POST', 'GET'])
def tansaction():
    amount = request.form["amount"]
    print(amount)
    return jsonify({'result':'ok'}), 200

        