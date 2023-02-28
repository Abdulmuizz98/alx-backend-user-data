#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Returns a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        """
        from sqlalchemy.exc import InvalidRequestError
        from sqlalchemy.orm.exc import NoResultFound
        key, value = list(kwargs.items())[0]

        if key not in ['id', 'email', 'session_id', 'reset_token']:
            raise InvalidRequestError()
        if key == 'email':
            user = self._session.query(User).filter_by(email=value).first()
        if key == 'id':
            user = self._session.query(User).filter_by(id=value).first()
        if key == 'session_id':
            v = value
            user = self._session.query(User).filter_by(session_id=v).first()
        if key == 'session_id':
            v = value
            user = self._session.query(User).filter_by(reset_token=v).first()

        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in ['email', 'hashed_password', 'session_id', 'reset_token']:
                raise ValueError
            setattr(user, k, v)
        self._session.commit()
        return None
