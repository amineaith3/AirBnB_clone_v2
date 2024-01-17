#!/usr/bin/python3
""" New engine DBStorage module """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """ New engine DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Create the engine (self.__engine)
        the engine must be linked to the MySQL database and user created before (hbnb_dev and hbnb_dev_db) """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session) all objects depending on the class name (argument cls)
        if cls=None, query all types of objects (User, State, City, Amenity, Place, and Review) """
        data = {}
        if cls:
            for obj in self.__session.query(eval(cls)).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                data[key] = obj
        else:
            for cls in [User, State, City, Amenity, Place, Review]:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    data[key] = obj
        return data

    def new(self, obj):
        """ add the object to the current database session (self.__session) """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session (self.__session) """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database (feature of SQLAlchemy) (WARNING:
        all classes who inherit from Base must be imported before
        calling Base.metadata.create_all(engine)) """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()
