from .models import Dogs, PointOfInterests, User, DogBreeds
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .observer_pattern import MapState, MapView, Observer

current_map_state = MapState()
# current_map_view = MapView


@login_required
def home(request):
    return render(request, 'dog_walker/home.html')



# def login(request):
#     return render(request, 'dog_walker/login.html', {'title': 'Login'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('dog_walker-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'dog_walker/register.html', {'title': 'Register', 'form': form})


def view_map(request):
    current_map_view = MapView()
    print(request.user)
    current_map_view.set_id(request.user)
    current_map_state.register(current_map_view)
    # for observer in current_map_state.get_all_observers():
    #     print(observer.id)
    return render(request, 'dog_walker/view_map.html', {'title': 'View Map'})


@login_required
def add_a_dog(request):
    if request.method == 'POST':
        age = 2019 - int(request.POST.get('dog_birthday')[:4])
        temp_dict = {
            'user_id': User.objects.get_by_natural_key(request.user),
            'dog_name': request.POST.get('dog_name').capitalize(),
            'dog_breed_id': DogBreeds.objects.get(breed_name=request.POST.get('dog_breed')),
            'dog_age': age,
            'dog_weight': request.POST.get('dog_weight'),
            'dog_image': 'https://upload.wikimedia.org/wikipedia/commons/4/4c/Chihuahua1_bvdb.jpg'
        }
        Dogs.objects.create(**temp_dict)

    dog_breeds = []
    for dog_breed in DogBreeds.objects.all():
        dog_breeds.append(dog_breed.breed_name)
    content = {
        'title': 'Add A Dog',
        'dog_breeds': dog_breeds,
    }
    return render(request, 'dog_walker/add_a_dog.html', content)


@login_required
def add_a_poi(request):
    if request.method == 'POST':
        temp_dict = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'creator': User.objects.get_by_natural_key(request.user),
            'location': 'SRID=4326;POINT ({} {})'.format(
                request.POST.get('lng'), request.POST.get('lat')),
            'category': request.POST.get('category'),
            'is_private': True if request.POST.get('is_private') == 'yes' else False,
        }
        PointOfInterests.objects.create(**temp_dict)
        current_map_state.notify()

    return render(request, 'dog_walker/add_a_poi.html', {'title': 'Add A POI'})


def generate_walking_route(request):
    return render(request, 'dog_walker/generate_walking_route.html', {'title': 'Generate a Route'})


@login_required
def my_dogs_homepage(request):
    current_user = request.user
    dog_list = Dogs.objects.filter(user_id=current_user)
    dogs = []
    for dog in dog_list:
        dogs.append(
            {
                'name': dog.dog_name,
                'breed': dog.dog_breed_id,
                'age': dog.dog_age,
                # 'weight': dog.dog_weight,
                'image': dog.dog_image,
            },
        )
    content = {
        'title': 'My Dogs',
        'dogs': dogs,
    }
    return render(request, 'dog_walker/my_dogs_homepage.html', content)

@login_required
def dog_info(request):
    return render(request, 'dog_walker/dog_info.html', {'title': 'Dog Info'})


@login_required
def display_route(request):
    points = []
    if request.method == 'POST':
        points.append(PointOfInterests.objects.filter(name=request.POST.get('start_point'))[0].location)
        points.append(PointOfInterests.objects.filter(name=request.POST.get('end_point'))[0].location)
    content = {
        'title': 'Display Route',
        'start_point': PointOfInterests.objects.filter(name=request.POST.get('start_point'))[0].location,
        'end_point': PointOfInterests.objects.filter(name=request.POST.get('end_point'))[0].location,
        'points': points
    }
    return render(request, 'dog_walker/display_route.html', content)

@login_required
def generate_walking_route(request):
    poi_list = PointOfInterests.objects.all()
    point_names = []
    for point in poi_list:
        point_names.append(point.name)
    content = {
        'title': 'Make Walking Route',
        'point_names': point_names,
    }
    return render(request, 'dog_walker/generate_walking_route.html', content)



