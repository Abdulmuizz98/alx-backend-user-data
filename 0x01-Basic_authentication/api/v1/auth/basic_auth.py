#!/usr/bin/env python3
""" Contains the class BasicAuth to manage api authorization
"""

# from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Defines the BasicAuth object
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the Base64 part of the Authorization header
        """
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Returns the decoded value of base64 string
        """
        from base64 import b64encode as en, b64decode as dec
        if not base64_authorization_header or \
           type(base64_authorization_header) is not str:
            return None
        try:
            return dec(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Returns the user email and password from base64 decoded value
        """
        if not decoded_base64_authorization_header or \
           type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        from models.user import User
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        user_list = User.search({'email': user_email})
        if user_list == []:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request
        """
        ah_value: str = self.authorization_header(request)
        base64_value: str = self.extract_base64_authorization_header(ah_value)
        raw_value: str = self.decode_base64_authorization_header(base64_value)
        user_cred: str = self.extract_user_credentials(raw_value)
        return self.user_object_from_credentials(*user_cred)
