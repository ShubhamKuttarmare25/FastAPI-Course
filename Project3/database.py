#it used to create url string to connect to database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db' # this will be automatically created no need to explicitely create this 

#create engine to run application
#for sqlite, we use sqlite:///./<filename> format
#sqlite will allow only one connection at a time, so we need to set check_same_thread to False
#each thread will handle indipendent requests
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False})

#create a session local class to create session for each request
#autocommit and autoflush are set to False to control transaction manually ohterwise it will commit automatically
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#create a base class for declarative models
#this will be used to create tables in the database
#all models will inherit from this base class
Base = declarative_base()

