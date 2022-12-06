import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat.routing
import notification.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaggamagga.settings")
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter( # ProtocolTypeRouter는 어떤 프로토콜로 연결이 됐는지 파악하고 해당 프로토콜의 미들웨어로 연결해준다.
    {
        # "http": get_asgi_application(),
        "http": django_asgi_app,
        "websocket" : AuthMiddlewareStack(
            # AuthMiddlewareStack은 인증된 유저 여부에 따라 연결의 scope를 제한한다.
            URLRouter(
                [*notification.routing.websocket_urlpatterns, *chat.routing.websocket_urlpatterns] # 언패킹
            )
        ),
        # "websocket" : AuthMiddlewareStack(
        #     URLRouter(
        #         chat.routing.websocket_urlpatterns
        #     )
        # )
    }
)