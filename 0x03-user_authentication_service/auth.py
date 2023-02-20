#!/usr/bin/env python3
"""Contains the Authorization and Authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return new string uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        try:
            old_user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials
        """
        try:
            exists_user = self._db.find_user_by(email=email)
            hashed_pwd = exists_user.hashed_password
            return bcrypt.checkpw(password.encode(), hashed_pwd)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session and return its id
        """
        try:
            user = self._db.find_user_by(email=email)
            user_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=user_uuid)
            return user_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id: str) -> None:
        """Get user from session_id
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
