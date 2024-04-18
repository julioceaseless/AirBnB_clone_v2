#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import environ


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship(
                'City', cascade='all, delete, delete-orphan',
                backref='state')
    else:
        @property
        def cities(self):
            """
            getter method for cities
            returns the list of Cities where state_id equals
            self.id
            """
            from models import storage
            from models.city import City
            related_cities = []
            cities_dict = storage.all(City)
            for city in cities_dict.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities
