from django.urls import path
from django.conf.urls import include, url
from . import views, datasets
urlpatterns = [
    # Pages
    path('', views.home, name='dog_walker-home'),
    path('about/', views.about, name='dog_walker-about'),
    path('login/', views.login, name='dog_walker-login'),
    path('register/', views.register, name='dog_walker-register'),
    path('view_map/', views.view_map, name='dog_walker-view_map'),
    path('my_dogs_homepage/', views.my_dogs_homepage, name='dog_walker-my_dogs_homepage'),
    path('dog_info/', views.dog_info, name='dog_walker-dog_info'),
    path('add_a_dog/', views.add_a_dog, name='dog_walker-add_a_dog'),
    path('generate_walking_route/', views.generate_walking_route, name='dog_walker-generate_walking_route'),

    # Datasets
    path('point_of_interest_dataset/', datasets.point_of_interest_dataset, name='poi_dataset'),
    path('dog_breed_dataset/', datasets.dog_breed_dataset, name='dog_breed_dataset'),
    path('dogs_dataset/', datasets.dogs_dataset, name='dogs_dataset'),
]
