import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from lucky_club.database import db


class Profile(db.Model):
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    photo_file_name = Column(String(500), nullable=True)
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User', backref=db.backref('user_profile', uselist=False, lazy='select'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(String(255), nullable=True)
    bank_card = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)

    @property
    def photo_url(self):
        if self.photo_file_name:
            from lucky_club.lucky_club import uploaded_photos
            return uploaded_photos.url(self.photo_file_name)
        else:
            return ""

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'screen_name': self.screen_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo_url': self.photo_url,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'email': self.updated_at,
            'bank_card': self.updated_at,
            'phone': self.updated_at
        }
