from dataclasses import dataclass
from datetime import datetime
import app


@dataclass
class User(app.db.Model):
    # id : int
    # username : str
    # password : str
    # date: datetime
    # admin :bool

    id = app.db.Column(app.db.Integer(), primary_key=True, autoincrement=True)
    username = app.db.Column(app.db.String(140))
    password = app.db.Column(app.db.String(140))
    date = app.db.Column(app.db.DateTime(), default=datetime.now())
    admin = app.db.Column(app.db.Boolean(), default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<User id:{self.id} - {self.username}'

@dataclass
class Debtor (app.db.Model):
    # debtor_id : int
    # name : str
    # lastname : str
    # date: datetime

    debtor_id = app.db.Column(
        app.db.Integer(), primary_key=True, autoincrement=True)
    name = app.db.Column(app.db.String(140))
    lastname = app.db.Column(app.db.String(140))
    date = app.db.Column(app.db.DateTime(), default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'debtor_id:{self.debtor_id} - {self.name}'


@dataclass
class Transaction (app.db.Model):
    # trans_id : int
    # id : int
    # debtor_id : int
    # amount : float
    # trans_type : str
    # trans_date : datetime
    # status : str
    # updated_at : datetime
    # updated_by : int

    trans_id = app.db.Column(
        app.db.Integer(), primary_key=True, autoincrement=True)
    id = app.db.Column(app.db.Integer, app.db.ForeignKey(
        'user.id'), nullable=False)
    debtor_id = app.db.Column(app.db.Integer, app.db.ForeignKey(
        'debtor.debtor_id'), nullable=True)
    amount = app.db.Column(app.db.Float)
    name = app.db.Column(app.db.String(50))
    trans_date = app.db.Column(app.db.DateTime(), default=datetime.now())
    status = app.db.Column(app.db.String(50))
    updated_at = app.db.Column(app.db.DateTime(), default=datetime.now())
    updated_by = app.db.Column(
        app.db.Integer, app.db.ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'Transaction_id:{self.trans_id} - {self.name}'
