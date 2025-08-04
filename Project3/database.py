#it used to create url string to connect to database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' # this will be automatically created no need to explicitely create this 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False})


SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


Base = declarative_base()

