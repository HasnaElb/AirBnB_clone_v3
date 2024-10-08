#!/usr/bin/python3
""" This is the database storage """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import Sqlalchemy

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage():
    """ This is the DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiation of DBStorage class """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
		format(HBNB_MySQL_USER,
		HBNB_MYSQL_PWD,
		HBNB_MYSQL_HOST, MYSQL_DB), pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Show all class objects in DBStorage or specified class if given
        """
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            objects = []
            for c in classes:
                objects += self.__session.query(c)
        my_dict = {}
        for obj in objects:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """ Add the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current database
        session from the engine """
        # Base.metadata.create_all(self.__engine)  # redundant with __init__?
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Closes current SQLAlchemy session, discarding unsaved changes and
        updating `storage` with current state of DB.

        Project: 0x04. AirBnB clone - Web framework
        Task: 7. Improve engines
        """
        self.__session.close()
    def get(self, cls, id):
        """ Returns specified object from database.

        Args:
            cls (<BaseModel-derived>): class of object to return
            id (str): uuid of object to return

        Returns:
            `BaseModel`-derived object of UUID `id` from database.
        """
        if cls in classes.values() and id and type(id) is str:
            return (self.__session.query(cls).get(id))

    def count(self, cls=None):
        """ Returns count of all objects of a given type, or grand total if no
        type given.

        Args:
            cls (<BaseModel-derived>): class of object to return

        Returns:
            Total count of all objects in database of type `cls`, or total of
        all objects if no type given.
        """
        if cls is None:
            return (len(self.all()))
        return (len(self.__session.query(cls).all()))
