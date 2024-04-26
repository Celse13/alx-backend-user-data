#!/usr/bin/env python3
"""Module of auth"""
from db import DB
import bcrypt
from uuid import uuid4
from user import User
from typing import ByteString
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for a user"""
        user = self._db.find_user_by(email=email)
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get a user from a session ID"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session"""
        self._db.update_user(user_id, session_id=None)
        return None
