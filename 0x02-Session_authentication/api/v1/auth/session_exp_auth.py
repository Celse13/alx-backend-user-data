#!/usr/bin/env python3
"""SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth"""

    def __init__(self):
        """Initialize a new SessionExpAuth instance"""
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID"""
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        if 'created_at' not in session_dictionary:
            return None

        if datetime.now() > session_dictionary.get('created_at') + \
                timedelta(seconds=self.session_duration):
            return None

        return session_dictionary.get('user_id')
