#!/usr/bin/env python3
""" Contains the class BasicAuth to manage api authorization
"""

# from flask import request
# from typing import TypeVar, List
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
        return tuple(decoded_base64_authorization_header.split(':'))
