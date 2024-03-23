#!/usr/bin/python3
"""
This is a Package initializer
"""
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':  # if storage type is database
    from models.engine.db_storage import DBStorage as Storage
else:
    from models.engine.file_storage import FileStorage as Storage

storage = Storage()
storage.reload()
