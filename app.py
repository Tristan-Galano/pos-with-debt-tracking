from flask import Flask, jsonify, render_template, redirect, request, session, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.secret_key = ['sadsadsadsafgfhjtrew23456uiutjyhg']

import models

app.app_context().push()


@app.route("/")
def home():
    if session.get('id'):
        return redirect('cashier')
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        return redirect('/')

    if username == user.username and password == user.password:
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
        username=fullname,
        password=password,
        admin=role
    )
    db.session.add(user)
    db.session.commit()
    return redirect('/cashier')


@app.route("/cashier")
def cashier():

    if session.get('username'):

        debtors = models.Debtor.query.all()
        return render_template('cashier.html', debtors=debtors)

    else:
        return redirect('/')


@app.route("/debtor", methods=['POST', 'GET'])
def debtor():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        debtor = models.Debtor(
            name=firstname,
            lastname=lastname
        )
        db.session.add(debtor)
        db.session.commit()
        return redirect('/')
    if session.get('id'):
        return render_template('debtor.html')
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('admin', None)
    return redirect('/')

@app.route('/report', methods=['POST','GET'])
def report():
    transactions_with_details = (
    db.session.query(
        models.Transaction.trans_id,
        models.User.username,
        models.Debtor.name.label("debtor_name"),  # Adding debtor's name to the query
        models.Transaction.amount,
        models.Transaction.Transaction_type,
        models.Transaction.trans_date,
        models.Transaction.status,
        models.Transaction.updated_at,
        models.Transaction.updated_by,
    )
    .join(models.User, models.Transaction.id == models.User.id)  # Join with User table on user ID
    .outerjoin(models.Debtor, models.Transaction.debtor_id == models.Debtor.debtor_id)  # Outer join with Debtor table on debtor_id
    .all()
)
    
    return render_template('report.html',records = transactions_with_details)


@app.route('/tansaction', methods=['POST'])
def tansaction():

    fullname = request.form['namelist']
    amount = request.form['amount']
    debtor_id = None
    user_id = session['id']
    trans_type = "sale"
    status = "Completed"
    updated_by = user_id

    if fullname:
        trans_type = "credit"
        debtor = models.Debtor.query.filter(
            models.Debtor.name + ' ' + models.Debtor.lastname == fullname).first()
        debtor_id = debtor.debtor_id

    transaction = models.Transaction(
        id=user_id,
        debtor_id=debtor_id,
        amount=amount,
        trans_type=trans_type,
        status=status,
        updated_by=updated_by
    )

    if amount:
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'result': 'ok'}), 200

    return jsonify({'result': 'not ok'}), 200
