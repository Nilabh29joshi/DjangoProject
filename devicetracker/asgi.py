"""
ASGI config for devicetracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# devicetracker/asgi.py

# devicetracker/asgi.py

# devicetracker/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from tracking.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devicetracker.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # This line handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

