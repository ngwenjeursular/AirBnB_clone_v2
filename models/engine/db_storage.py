from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """This class manages storage of hbnb models using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new instance of DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objs = {}
        if cls:
            for obj in self.__session.query(eval(cls)).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs[key] = obj
        else:
            for cls in Base.__subclasses__():
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj
        return objs

    def new(self, obj):
        """Adds new object to storage session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads objects from the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.close()
