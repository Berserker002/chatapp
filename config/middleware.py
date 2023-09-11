from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from django.utils import timezone

class TokenAuthenticationError(Exception):
    pass


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None
    

@database_sync_to_async
def get_expiration_time(user):
    try:
        return user.auth_token.created + timezone.timedelta(hours=1)
    except Token.DoesNotExist:
        return None
    
@database_sync_to_async
def set_user_offline(user):
     user.is_online = False
     user.save()

class WebSocketTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):


        if scope.get("type") == "websocket":
            query_string = scope.get("query_string", b"").decode("utf-8")
            token_key = None

            if "token=" in query_string:
                token_key = query_string.split("token=")[1]

            if not token_key:
                headers = dict(scope["headers"])
                auth_header = headers.get(b"authorization", b"").decode("utf-8")
                if auth_header.startswith("Token "):
                    token_key = auth_header.split("Token ")[1]
            if token_key:
                user = await get_user(token_key)
                
                if user:
                    current_time = timezone.now()
                    token_expiration_time = await get_expiration_time(user)
                    if current_time >= token_expiration_time:
                       await set_user_offline(user)

                    scope["user"] = user
                else:
                    raise TokenAuthenticationError("Invalid token")

        return await super().__call__(scope, receive, send)
