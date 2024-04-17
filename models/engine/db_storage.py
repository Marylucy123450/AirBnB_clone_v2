#!/usr/bin/python3
"""This module defines the DBStorage class"""

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import json

import os


class DBStorage:
    """A class for interacting with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and session"""

        try:
            USER = os.getenv('HBNB_MYSQL_USER')
            PWD = os.getenv('HBNB_MYSQL_PWD')
            HOST = os.getenv('HBNB_MYSQL_HOST')
            DB = os.getenv('HBNB_MYSQL_DB')

            # verify we got all neccessary attributes
            mandatory = [USER, PWD, HOST, DB]
            for i in mandatory:
                if i is None:
                    print("Missing mandatory environment variable")

            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                USER, PWD, HOST, DB),
                pool_pre_ping=True)

            ENV = os.environ.get('HBNB_ENV')
            if (ENV == 'test'):
                Base.metadata.drop_all(bind=self.__engine, checkfirst=True)

        except Exception as e:
            print("raised exception in base_model init")
            print(e)

    def all(self, cls=None):
        """
        Query the current session and list all instances of cls
        """
        classes = [State, City, User, Place, Review, Amenity]

        if cls is None:
            query_classes = classes
        else:
            query_classes = [cls]

        query_result = self.__session.query(*query_classes).all()

        # return the results as a dictionary with class.id as key
        return {"{}.{}".format(result.__class__.__name__, result.id): result
                for result in query_result}

    def new(self, obj):
        """add object to current session
        """
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """commit current done work
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None
        """
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """reload the session
        """
        try:
            Base.metadata.create_all(self.__engine)
            Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Scope = scoped_session(Session)
            self.__session = Scope()
        except Exception as e:
            print(e)

    def close(self):
        """Close the session."""
        self.__session.close()
