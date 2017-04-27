import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Numeric
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Lot(Base):
    __tablename__ = 'Lot'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    category_id = Column(ForeignKey('Category.id'))
    category = relationship('Category')
    owner_id = Column(ForeignKey('User.id'))
    owner = relationship('User')
    closed = Column(Boolean, default=False, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    winner_id = Column(ForeignKey('User.id'))
    winner = relationship('User')
    count_participants = Column(Integer, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id':self.category_id,
            'closed': self.closed,
            'deleted': self.deleted,
            'winner_id': self.winner_id,
            'count_participants': self.count_participants,
            'price': self.price,
            'owner_id': self.owner_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Participants(Base):
    __tablename__ = 'Participants'

    id = Column(Integer, primary_key=True)
    lot_id = Column(ForeignKey('Lot.id'))
    lot = relationship('Lot')
    participant_id = Column(ForeignKey('User.id'))
    participant = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'participant_id':self.participant_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Favorite(Base):
    __tablename__ = 'Favorite'

    id = Column(Integer, primary_key=True)

    lot_id = Column(ForeignKey('Lot.id'))
    lot = relationship('Lot')
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Messages(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True)
    message = Column(String(255))

    lot_id = Column(ForeignKey('Lot.id'))
    lot = relationship('Lot')
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'message':self.message,
            'lot_id':self.lot_id,
            'user_id':self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }