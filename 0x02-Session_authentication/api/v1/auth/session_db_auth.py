#!/usr/bin/env python3
""" SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """
        method that creates and stores new instance of UserSession
        Returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        method that returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_id = user_session[0].user_id
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        method that destroys the UserSession based on the
        Session ID from the request cookie
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_session = UserSession.search({'session_id': session_id})
                if user_session:
                    user_session[0].remove()
