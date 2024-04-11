#!/usr/bin/env python3
"""Hash a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """password hashing"""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """password validation"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
 
