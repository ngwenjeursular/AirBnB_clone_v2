""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade="all, delete", backref="place")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False, backref="place_amenities")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = kwargs.get('id', "")
        self.city_id = kwargs.get('city_id', "")
        self.user_id = kwargs.get('user_id', "")
        self.name = kwargs.get('name', "")
        self.description = kwargs.get('description', "")
        self.number_rooms = kwargs.get('number_rooms', 0)
        self.number_bathrooms = kwargs.get('number_bathrooms', 0)
        self.max_guest = kwargs.get('max_guest', 0)
        self.price_by_night = kwargs.get('price_by_night', 0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        self.amenity_ids = []

    def get_city(self):
        """Get the City instance associated with this Place"""
        from models import storage
        city = storage.get(City, self.city_id)
        return city
