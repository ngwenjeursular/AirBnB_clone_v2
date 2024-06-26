#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="delete", backref="state")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = kwargs.get('id', "")

    @property
    def cities(self):
        """ Getter method to retrieve related City instances """
        from models import storage
        city_instances = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                city_instances.append(city)
        return city_instances
