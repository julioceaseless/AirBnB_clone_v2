#!/usr/bin/python3
"""engine for database storage"""
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from os import getenv


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """initialize a new database storage object """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """ Shows all instances of the given class or all all classes"""
        all_classes = ["State", "City", "User", "Place", "Review", "Amenity"]
        list_objs = []
        dict_objs = {}
        if cls and cls in all_classes:
            list_objs = self.__session.query(eval(cls)).all()
        else:
            for each_class in all_classes:
                cls = eval(each_class)
                list_objs += self.__session.query(cls).all()
        for obj in list_objs:
            key = f'{obj.__class__.__name__}.{obj.id}'
            dict_objs[key] = obj
        return dict_objs

    def new(self, obj):
        """ add obj to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes obj to the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ calls remove to dispose of the current session, if present"""
        self.__session.remove()
