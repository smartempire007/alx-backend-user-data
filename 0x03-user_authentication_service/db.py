#!/usr/bin/env python3
"""DB module
"""

# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # Create an engine object to handle the database connection
        self._engine = create_engine("sqlite:///a.db")

        # Drop all existing tables and create new tables
        # based on the declared models
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

        # Initialize session as None at the beginning
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        # If session is not yet created, create a new session
        # and bind it to the engine
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds user to db """
        # Create a new User object with the provided email and hashed_password
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        self._session.add(new_user)

        # Commit the changes to the database
        self._session.commit()

        # Return the newly added user object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Returns first row found in users table based on keyword args """

        try:
            # Query the user table based on the keyword arguments provided
            record = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            # If any error occurs during the query, raise an InvalidRequestError
            raise InvalidRequestError

        if record is None:
            """If no user is found with the given criteria,
            raise a NoResultFound exception"""
            raise NoResultFound

        # Return the found user object
        return record

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Finds user record and updates attributes """
        # Find the user record based on the provided user_id
        user_record = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user_record, key):
                # If the attribute exists in the user_record,
                # update its value with the provided value
                setattr(user_record, key, value)
            else:
                # If the attribute does not exist in the user_record,
                # raise a ValueError
                raise ValueError

        # Commit the changes to the database
        self._session.commit()

        # Return None after successfully updating the user record
        return None
