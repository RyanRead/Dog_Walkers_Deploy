from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='map-home'),
    path('view_map/', views.view_map, name='map-view_map'),
]
