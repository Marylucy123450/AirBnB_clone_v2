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

import os

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


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
            print("raised exception in DBStorage init")
            print(e)


    def all(self, cls=None):
        """Query all objects from the current database session."""
        new_dict = {}
        for class_name, class_obj in classes.items():
            # If cls is None, or
            # If cls is a string representing the current class (class_name), or
            # If cls is the class object itself (class_obj),
            if cls is None or isinstance(cls, str) and cls == class_name or cls is class_obj:
                objs = self.__session.query(class_obj).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj
        return new_dict


    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit current done work
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None
        """
        if obj is not None:
            self.__session.delete(obj)

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
        """call remove() method on the private session attribute"""
        self.__session.remove()
