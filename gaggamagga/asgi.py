import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat.routing
import notification.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaggamagga.settings")
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        # "http": get_asgi_application(),
        "http": django_asgi_app,
        # "websocket": AllowedHostsOriginValidator(
        #     AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        # ),
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                notification.routing.websocket_urlpatterns
            )
        )
    }
)