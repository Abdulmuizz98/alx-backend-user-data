#!/usr/bin/env python3
"""Contains the function bcrypt """


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password which is a byte string."""
    from bcrypt import hashpw, gensalt
    return hashpw(bytes(password, 'utf-8'), gensalt())
