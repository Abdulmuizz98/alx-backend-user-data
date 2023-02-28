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

    def get_user_from_session_id(self, session_id: str) -> None:
        """Get user from session_id
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a user session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset_token and returns it
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_uuid = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_uuid)
            return reset_uuid
        except NoResultFound:
            raise ValueError('User DNE')

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a usesr password by verifying reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd)
            self._db.update_user(user.id, reset_token=None)
            return None
        except NoResultFound:
            raise ValueError('User DNE')
