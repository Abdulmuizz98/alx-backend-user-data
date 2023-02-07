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
