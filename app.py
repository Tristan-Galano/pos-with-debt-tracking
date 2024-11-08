from flask import Flask, jsonify, render_template,redirect, request, session, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
    if user is None:
        return redirect('/')
    
    if username == user.username and password==user.password:
        session['id'] = user.id
        session['username'] = username
        session['admin'] = user.admin
        return redirect('/cashier')
    else:
        return redirect('/')

@app.route("/sign-up")
def sign_up():

    if session.get('admin'):
        if session['admin'] == True:
            return render_template("signup.html")
    else:
        return redirect('/cashier')
    
@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    role = request.form['role']
    fullname = request.form['fullname']
    password = request.form['password']
    if role != 'user':
        role = True
    else:
        role = False
        
    user = models.User(
        username = fullname,
        password = password,
        admin = role
    )
    db.session.add(user)
    db.session.commit()
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
    
    fullname = request.form['namelist']
    amount = request.form['amount']
    debtor_id = None
    user_id = session['id']
    trans_type = "sale"
    status = "Completed"
    updated_by = user_id
    
    if fullname:
        trans_type="credit" 
        debtor = models.Debtor.query.filter(models.Debtor.name+ ' ' + models.Debtor.lastname==fullname).first()
        debtor_id = debtor.debtor_id
    
    transaction = models.Transaction(
        id = user_id,
        debtor_id = debtor_id,
        amount = amount,
        name = trans_type,
        status = status,
        updated_by = updated_by   
    )
    
    if amount:
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'result':'ok'}), 200
    
    return jsonify({'result':'not ok'}), 200