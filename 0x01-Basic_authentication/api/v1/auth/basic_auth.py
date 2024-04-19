#!/usr/bin/env python3
"""BasicAuth class"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Method that returns the Base64 part of the Authorization header"""
        if authorization_header is None or \
                type(authorization_header) != str or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
