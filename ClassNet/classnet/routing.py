from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classnet.settings')

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "http": get_asgi_application(), 
    'websocket': AuthMiddlewareStack(
        URLRouter(            
            chat.routing.websocket_urlpatterns
        )
    ),
})
