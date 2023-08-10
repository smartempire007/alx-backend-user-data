#!/usr/bin/env python3
"""
Module for authentication using Basic auth
"""

from typing import Optional, Tuple, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(
            self, authorization_header: Optional[str]) -> Optional[str]:
        """
        Extracts the base64 authorization header from the provided
        header string.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The extracted base64 authorization token.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(
            self, base64_authorization_header: Optional[str]) -> Optional[str]:
        """
        Decodes the base64 authorization header and returns the decoded string.

        Args:
            base64_authorization_header (str): The base64 authorization header.

        Returns:
            str: The decoded authorization header string.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header:
            Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the email and password from the decoded base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded base64
            authorization header.

        Returns:
            Tuple[str, str]: The email and password as a tuple.
        """
        # if decoded_base64_authorization_header is None or not isinstance(
        #         decoded_base64_authorization_header, str):
        #     return (None, None)
        # if ':' not in decoded_base64_authorization_header:
        #     return (None, None)

        # email, password = decoded_base64_authorization_header.split(':')
        # return (email, password)
        if decoded_base64_authorization_header is None:
            return None, None
        if isinstance(decoded_base64_authorization_header, str) is False:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1)[:2])

    def user_object_from_credentials(self,
                                     user_email: Optional[str],
                                     user_pwd: Optional[str]
                                     ) -> Optional[TypeVar('User')]:
        """
        Retrieves the user object based on the provided email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The user object if found, else None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the current user based on the provided request object.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            User: The current user object if authenticated, else None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return None
