"""Authentication classes for channels."""
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode

import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class JWTAuthMiddleware:
    """Middleware to authenticate user for channels"""

    def __init__(self, app):
        """Initializing the app."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Authenticate the user based on jwt."""
        close_old_connections()
        try:
            # Decode the query string and get token parameter from it.
            query_string = scope.get("query_string", b"").decode("utf-8")
            query_params = parse_qs(query_string)
            token = query_params.get("token", [None])[0]
            # token = parse_qs(scope["query_string"].decode("utf8")).get('token', None)[0]
            
            if not token:
                raise ValueError("No token provided")

            # Decode the token to get the user id from it.
            payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get('token_type') != 'access':
                raise ValueError("Invalid token type")
            
            # Get the user from database based on user id and add it to the scope.
            # scope['user'] = await self.get_user(data['user_id'])
            scope['user'] = await self.get_user(payload['user_id'])

        # except (TypeError, KeyError, InvalidSignatureError, ExpiredSignatureError, DecodeError):
        #     # Set the user to Anonymous if token is not valid or expired.
        #     scope['user'] = AnonymousUser()

        except (ValueError, IndexError, KeyError) as e:
            logger.debug(f"Token validation error: {str(e)}")
            scope['user'] = AnonymousUser()
        except (InvalidSignatureError, DecodeError):
            logger.warning("Invalid token signature")
            scope['user'] = AnonymousUser()
        except ExpiredSignatureError:
            logger.debug("Token expired")
            scope['user'] = AnonymousUser()
        except Exception as e:
            logger.error(f"Unexpected authentication error: {str(e)}")
            scope['user'] = AnonymousUser()
            
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """Return the user based on user id."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """This function wrap channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))