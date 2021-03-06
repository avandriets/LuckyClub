import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Numeric
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from lucky_club.database import db


class Lot(db.Model):
    __tablename__ = 'Lot'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    full_description = Column(Text)
    category_id = Column(ForeignKey('Category.id'))
    category = relationship('Category', backref=db.backref('lots_of_category', lazy='select'))
    owner_id = Column(ForeignKey('User.id'))
    owner = relationship('User', backref=db.backref('user_lots', lazy='select'), foreign_keys='Lot.owner_id')
    published = Column(Boolean, default=False, nullable=False)
    finished = Column(Boolean, default=False, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    winner_id = Column(ForeignKey('User.id'))
    winner = relationship('User', backref=db.backref('user_winner', lazy='select'), foreign_keys='Lot.winner_id')
    recommend = Column(Boolean, default=False, nullable=False)
    count_participants = Column(Integer, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def count_joined(self):
        count_members = Participants.query.filter_by(lot_id=self.id).count()
        return count_members

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'full_description': self.full_description,
            'category_id': self.category_id,
            'published': self.published,
            'finished': self.finished,
            'deleted': self.deleted,
            'winner_id': self.winner_id,
            'count_participants': self.count_participants,
            'price': self.price,
            'owner_id': self.owner_id,
            'recommend': self.recommend,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'pictures': [c.serialize for c in self.images_of_lot],
            'owner_profile': self.owner.user_profile.serialize,
            'count_joined': self.count_joined
        }


class Participants(db.Model):
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
            'participant_id': self.participant_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Favorite(db.Model):
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
            'lots': [c.serialize for c in self.lot],
            'lot_id': self.lot_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Messages(db.Model):
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
            'message': self.message,
            'lot_id': self.lot_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
