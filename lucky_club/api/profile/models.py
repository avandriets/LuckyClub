import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from lucky_club.database import Base


class Profile(Base):
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    photo_url = Column(String(500), nullable=True)
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo_url': self.photo_url,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
