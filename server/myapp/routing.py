from django.urls import re_path
from .consumers import SensorConsumer

websocket_urlpatterns = [
    re_path(r"ws/data/", SensorConsumer.as_asgi())
    # url('sensor/', SensorConsumer.as_asgi()),
]
