#!/usr/bin/env python3
"""
API session db module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth """

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session ID for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID.

        """

        pass

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with the provided session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or
            None if not found.
        """

        if session_id is None or isinstance(session_id, str) is False:
            return None
        else:
            pass

    def destroy_session(self, request=None):
        """
        Deletes the session associated with the provided request.

        Args:
            request (obj): The request object containing the session
            to be destroyed.

        Returns:
            None

        """
        pass
