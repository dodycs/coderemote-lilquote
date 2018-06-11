from sqlalchemy import or_, and_
from db.base import DbManager
from db.models import User, Quote

def get_all_quotes():
    db = DbManager()
    return db.open().query(Quote).all()

def get_all_quotes_for(user_id):
    db = DbManager()
    return db.open().query(Quote).filter(Quote.user_id == user_id).all()

def search_by_user_or_email(query):
    db = DbManager()
    return db.open().query(User).filter(or_(User.name.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    db = DbManager()
    quote = Quote()
    quote.content = content
    quote.user_id = user_id
    return db.save(quote)

def delete_quote(quote_id):
    db = DbManager()
    quote = db.open().query(Quote).filter(Quote.id == quote_id).one()
    quote = db.delete(quote)
    db.close()
    return quote

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filer(User.id == user_id).one()

def get_user_by_name(name):
    db = DbManager()
    return db.open().query(User).filter(User.name == name).one()

def get_user_by_email(user_email):
    db = DbManager()
    return db.open().query(User).filter(User.email == user_email).one()

def create_user(email, name, password):
    db = DbManager()
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)