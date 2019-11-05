from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, datasets
urlpatterns = [
    # Pages
    path('', auth_views.LoginView.as_view(template_name='dog_walker/login.html'), name='dog_walker-login'),
    path('home/', views.home, name='dog_walker-home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dog_walker/logout.html'), name='dog_walker-logout'),
    path('register/', views.register, name='dog_walker-register'),
    path('view_map/', views.view_map, name='dog_walker-view_map'),
    path('my_dogs_homepage/', views.my_dogs_homepage, name='dog_walker-my_dogs_homepage'),
    path('dog_info/<dog_name>/', views.dog_info, name='dog_walker-dog_info'),
    path('add_a_dog/', views.add_a_dog, name='dog_walker-add_a_dog'),
    path('add_a_poi/', views.add_a_poi, name='dog_walker-add_a_poi'),

    # Walking routes
    path('generate_walking_route/', views.generate_walking_route, name='dog_walker-generate_walking_route'),
    path('display_route/', views.display_route, name='dog_walker-display_route'),
    path('record_a_walk/', views.record_a_walk, name='dog_walker-record_a_walk'),
    path('record_a_walk_own_info/', views.record_a_walk_own_info, name='dog_walker-record_a_walk_own_info'),
    path('record_a_walk_saved_walking_route/', views.record_a_walk_saved_walking_route, name='dog_walker-record_a_walk_saved_walking_route'),

    # Walking Classes
    path('create_walking_class/', views.dog_trainer_create_a_class, name='dog_trainer-create_walking_class'),
    path('walking_classes/', views.walking_classes, name='dog_walker-walking_classes'),
    path('my_classes/', views.dog_trainer_my_classes, name='dog_trainer-my_classes'),
    path('view_class_detail_dog_walker/', views.view_class_detail_dog_walker, name='dog_walker-view_class_detail_dog_walker'),
    path('view_class_detail_dog_trainer/', views.view_class_detail_dog_trainer, name='dog_walker-view_class_detail_dog_trainer'),
    path('dog_trainer_home/', views.dog_trainer_home, name='dog_trainer-home'),

    # Datasets
    path('point_of_interest_dataset/', datasets.point_of_interest_dataset, name='poi_dataset'),
    # path('dog_breed_dataset/', datasets.dog_breed_dataset, name='dog_breed_dataset'),
    # path('dogs_dataset/', datasets.dogs_dataset, name='dogs_dataset'),
]
