#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
import uuid
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    current_time = datetime.utcnow
    created_at = Column(DateTime, default=current_time)
    updated_at = Column(DateTime, default=current_time)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            # Check if 'updated_at' key is present in kwargs
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()

            if '__class__' in kwargs:
                del kwargs['__class__']

            self.updated_at = kwargs['updated_at']
            self.created_at = kwargs['created_at']

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
