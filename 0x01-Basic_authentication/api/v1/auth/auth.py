#!/usr/bin/env python3
""" Contains the class Auth to manage api authorization
"""

from flask import request
from typing import TypeVar, List


class Auth:
    """
    """
    def __init__(self):
        """ Initializes the Auth class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Return True if path is not in excluded_paths
        """
        if path is None or excluded_paths in [None, []]:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            for i in excluded_paths:
                if i[-1] == '*' and path[:-1].startswith(i[:-1]):
                    return False
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Get value of request Authorization header
        """
        if not request or not request.headers.get('Authorization', None):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Not yet implemented Completely
        """
        return None
