from django.urls import path
from django.conf.urls import include, url
from . import views
urlpatterns = [
    path('', views.home, name='dog_walker-home'),
    path('about/', views.about, name='dog_walker-about'),
    path('view_map/', views.view_map, name='dog_walker-view_map'),
    path('my_dogs_homepage/', views.my_dogs_homepage, name='dog_walker-my_dogs_homepage'),
    path('dog_info/', views.dog_info, name='dog_walker-dog_info'),
    path('point_of_interest_dataset/', views.point_of_interest_datasets, name='poi_dataset')
]
