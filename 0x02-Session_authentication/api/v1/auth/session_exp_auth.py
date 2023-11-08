#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    class to add an expiration date to a Session ID
    """
    def __init__(self):
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", "0"))

    def create_session(self, user_id=None):
        """
        Create a Session ID and add it to the user_id_by_session_id dict
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user_id associated with the session_id if it's valid
        """
        if session_id is None or session_id not in \
                self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
