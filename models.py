from dataclasses import dataclass
from datetime import datetime
import app

@dataclass
class User(app.db.Model):
    __tablename__ = 'user'
    id = app.db.Column(app.db.Integer(), primary_key=True, autoincrement=True)
    username = app.db.Column(app.db.String(140))
    password = app.db.Column(app.db.String(140))
    date = app.db.Column(app.db.DateTime(), default=datetime.now())
    admin = app.db.Column(app.db.Boolean(), default=False)

    # Relationship to Transaction - user transactions and updates
    transactions = app.db.relationship('Transaction', back_populates='user', foreign_keys='Transaction.id')
    updated_transactions = app.db.relationship('Transaction', back_populates='updated_user', foreign_keys='Transaction.updated_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<User id:{self.id} - {self.username}>'

@dataclass
class Debtor(app.db.Model):
    __tablename__ = 'debtor'
    debtor_id = app.db.Column(app.db.Integer(), primary_key=True, autoincrement=True)
    name = app.db.Column(app.db.String(140))
    lastname = app.db.Column(app.db.String(140))
    date = app.db.Column(app.db.DateTime(), default=datetime.now())

    # Relationship to Transaction
    transactions = app.db.relationship('Transaction', back_populates='debtor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Debtor debtor_id:{self.debtor_id} - {self.name}>'

@dataclass
class Transaction(app.db.Model):
    __tablename__ = 'transaction'
    trans_id = app.db.Column(app.db.Integer(), primary_key=True, autoincrement=True)
    id = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'), nullable=False)
    debtor_id = app.db.Column(app.db.Integer, app.db.ForeignKey('debtor.debtor_id'), nullable=True)
    amount = app.db.Column(app.db.Float)
    Transaction_type = app.db.Column(app.db.String(50))
    trans_date = app.db.Column(app.db.DateTime(), default=datetime.now())
    status = app.db.Column(app.db.String(50))
    updated_at = app.db.Column(app.db.DateTime(), default=datetime.now())
    updated_by = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'), nullable=False)

    # Relationships to connect to User and Debtor models
    user = app.db.relationship('User', back_populates='transactions', foreign_keys=[id])
    updated_user = app.db.relationship('User', back_populates='updated_transactions', foreign_keys=[updated_by])
    debtor = app.db.relationship('Debtor', back_populates='transactions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Transaction trans_id:{self.trans_id} - {self.name}>'
