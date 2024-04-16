#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Method that returns False, path and excluded_paths will be used later
        '''
        return False

    def authorization_header(self, request=None) -> str:
        ''' Method that returns None, request will be the Flask request object
        '''
        return None

    def current_user(self, request=None) -> User:
        ''' Method that returns None, request will be the Flask request object
        '''
        return None
