from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='dog_walker-home'),
    path('about/', views.about, name='dog_walker-about'),
]
