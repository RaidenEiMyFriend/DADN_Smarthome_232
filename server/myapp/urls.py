# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboards/<str:document>/', views.fetch_collection_data, name='fetch-collection-data')
# ]
from django.urls import path
from .views import home
from .views import toggle_led
from .views import get_data

urlpatterns = [
    path('', home, name='home'),
    path('toggle-led/', toggle_led, name='toggle_led'),
    path('data/<str:data_type>/', get_data, name='get_data'),
]



