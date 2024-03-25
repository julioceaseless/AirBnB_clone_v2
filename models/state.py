#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                             cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            public getter to return list of City objects from storage
            that are linked to the current state
            """
            city_list = []
            city_objs = models.storage.all(City)
            for city in city_objs.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
