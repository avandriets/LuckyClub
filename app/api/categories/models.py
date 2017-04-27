import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from app.database import Base, db_session


class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    picture_url = Column(String(500), nullable=True)
    parent_id = Column(ForeignKey('Category.id'))
    parent = relationship('Category')
    user_id = Column(ForeignKey('User.id'))
    user = relationship('User')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture_url': self.picture_url,
            'parent_id': self.parent_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
