import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notification.routing 
# import app.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookwishes.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # "websocket":AuthMiddlewareStack(URLRouter(
        #     notification.routing.websocket_urlpatterns
        # ))
        "websocket":URLRouter(
            notification.routing.websocket_urlpatterns
        )
    }
)

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookwishes.settings')

# application = get_asgi_application()