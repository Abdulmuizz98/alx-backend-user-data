#!/usr/bin/env python3
"""Contains the Authorization and Authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
