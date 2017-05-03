import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from lucky_club.database import db


class Account(db.Model):
    __tablename__ = 'Account'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User', backref=db.backref('bank_account', uselist=False, lazy='select'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class AccountMovements(db.Model):
    __tablename__ = 'AccountMovements'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('Account.id'))
    account = relationship('Account')
    amount = Column(Numeric(8, 2), nullable=False)
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'account_id': self.account_id,
            'amount': self.amount,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }