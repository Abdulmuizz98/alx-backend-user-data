#!/usr/bin/env python3
"""Contains the function bcrypt """

from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password which is a byte string."""
    return hashpw(password.encode(), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password """
    return checkpw(password.encode(), hashed_password)
