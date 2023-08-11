#!/usr/bin/env python3
"""API session authentication module"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Session Authentication Class

    This class provides methods for creating and managing user sessions
    using session IDs.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create Session ID

        Generate a unique session ID for the specified user
        ID and store
        the mapping of session ID to user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID.
        """

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get User ID for Session ID

        Retrieve the user ID associated with the provided session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID.
        """

        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Get Current User

        Retrieve the User instance based on the cookie value in the request.

        Args:
            request: The request object containing the cookie.

        Returns:
            User: The User instance associated with the session ID
            in the cookie.
        """

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroy Session

        Delete the user session identified by the cookie value in
        the request.

        Args:
            request: The request object containing the cookie.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """

        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None or self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
