
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import WebSocketTokenAuthMiddleware
from app.routing import  websocket_urlpatterns
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({ 
    "http": get_asgi_application(),
    'websocket': WebSocketTokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})