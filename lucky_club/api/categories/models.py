import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from lucky_club.database import db


class Category(db.Model):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    picture_file = Column(String(500), nullable=True)
    parent_id = Column(ForeignKey('Category.id'), nullable=True)
    parent = relationship('Category', lazy="joined", join_depth=2)
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def picture_url(self):
        if self.picture_file:
            from lucky_club.lucky_club import uploaded_photos
            return uploaded_photos.url(self.picture_file)
        else:
            return ""

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture_file': self.picture_file,
            'picture_url': self.picture_url,
            'parent_id': self.parent_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
