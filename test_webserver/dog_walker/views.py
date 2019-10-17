from django.shortcuts import render
from .models import Dogs


def home(request):
    return render(request, 'dog_walker/home.html')


def login(request):
    return render(request, 'dog_walker/login.html', {'title': 'Login'})


def register(request):
    return render(request, 'dog_walker/register.html', {'title': 'Register'})


def about(request):
    return render(request, 'dog_walker/about.html', {'title': 'About'})


def view_map(request):
    return render(request, 'dog_walker/view_map.html', {'title': 'View Map'})


def add_a_dog(request):
    return render(request, 'dog_walker/add_a_dog.html', {'title': 'Add A Dog'})


def generate_walking_route(request):
    return render(request, 'dog_walker/generate_walking_route.html', {'title': 'Generate a Route'})


def my_dogs_homepage(request):
    data = Dogs.objects.all()
    dogs = []
    for dog in data:
        dogs.append(
            {
                'name': dog.dog_name,
                'breed': dog.dog_breed_id,
                'age': dog.dog_age,
                # 'weight': dog.dog_weight,
                'image': dog.dog_image,
            },
        )
    context = {
        'title': 'My Dogs',
        'dogs': dogs,
    }
    return render(request, 'dog_walker/my_dogs_homepage.html', context)


def dog_info(request):
    return render(request, 'dog_walker/dog_info.html', {'title': 'Dog Info'})



