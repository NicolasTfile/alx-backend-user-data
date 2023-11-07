#!/usr/bin/env python3
"""
implementation of Auth class
"""

from flask import request
from typing import TypeVar, List
from fnmatch import fnmatch


class Auth:
    """
    Auth class template for all API authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns True if the path is not in the list of strings excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        slashed_path = path if path.endswith("/") else path + "/"
        for pattern in excluded_paths:
            if fnmatch(slashed_path, pattern):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        return the value of the header request Authorization
        """
        auth_header = request.headers.get("Authorization")
        if request is None or auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request will be the Flask request object
        """
        None
