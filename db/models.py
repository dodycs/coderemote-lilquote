from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from db.base import Base, inverse_relationship, create_tables

class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   name = Column(String)
   email = Column(String, unique=True)
   password = Column(String)


class Quote(Base):
   __tablename__ = 'quote'

   id = Column(Integer, primary_key=True)
   quote = Column(String)

   user_id = Column(Integer, ForeignKey('user.id'))
   user = relationship(User, backref = inverse_relationship('quotes'))

if __name__ != '__main__':
   create_tables()