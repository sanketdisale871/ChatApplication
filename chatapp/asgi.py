
import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

import room.routing 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")




application = ProtocolTypeRouter({
    # For regular HTTP requests, use Django's get_asgi_application()
    "http": get_asgi_application(),
    # For WebSocket connections, use AuthMiddlewareStack with URLRouter
    "websocket": AuthMiddlewareStack(
        URLRouter(
            room.routing.websocket_urlpatterns
        )
    )
})
