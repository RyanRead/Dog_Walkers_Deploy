from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .observer_pattern import ConcreteObserver, ConcreteSubject
from .factory_method import *
from django.core.files.storage import FileSystemStorage


mySuccessFactory = ConcreteSuccessMessageCreator()
myErrorFactory = ConcreteErrorMessageCreator()

walking_Class_Subjects = ConcreteSubject()
users = User.objects.all()

for current_user in users:
    # print(User.email)
    walking_Class_Subjects.register(ConcreteObserver(current_user.username, current_user.email))


@login_required
def home(request):
    # TODO Add user to list if their not in the list
    return render(request, 'dog_walker/home.html')


@login_required
def dog_trainer_home(request):
    return render(request, 'dog_walker/dog_trainer_home.html', {'title': 'Dog Trainer Home'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('dog_walker-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'dog_walker/register.html', {'title': 'Register', 'form': form})


@login_required
def view_map(request):
    print(request.user)
    return render(request, 'dog_walker/view_map.html', {'title': 'View Map'})


@login_required
def add_a_dog(request):
    if request.method == 'POST':
        age = 2019 - int(request.POST.get('dog_birthday')[:4])
        if request.FILES['dog_image']:
            dog_image = request.FILES['dog_image']
            dog_image_name = dog_image.name
            save_file = FileSystemStorage()
            save_file.save(dog_image_name, dog_image)
        else:
            dog_image_name = 'default.png'

        temp_dict = {
            'user_id': User.objects.get_by_natural_key(request.user),
            'dog_name': request.POST.get('dog_name').capitalize(),
            'dog_breed_id': DogBreeds.objects.get(breed_name=request.POST.get('dog_breed')),
            'dog_age': age,
            'dog_weight': request.POST.get('dog_weight'),
            'dog_image': '/static/dogs/' + dog_image_name
        }
        Dogs.objects.create(**temp_dict)
        messages.success(request, mySuccessFactory.createProduct("add_dog").get_message())
        return redirect('dog_walker-my_dogs_homepage')

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
        messages.success(request, mySuccessFactory.createProduct("add_poi").get_message())
        return redirect('dog_walker-view_map')

    return render(request, 'dog_walker/add_a_poi.html', {'title': 'Add A POI'})


@login_required
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
                'image': dog.dog_image,
            },
        )
    content = {
        'title': 'My Dogs',
        'dogs': dogs,
    }
    return render(request, 'dog_walker/my_dogs_homepage.html', content)

@login_required
def dog_info(request, dog_name='default'):
    current_user = request.user
    selected_dog = Dogs.objects.filter(user_id=current_user, dog_name=dog_name)[0]
    dog = {
        'name': selected_dog.dog_name,
        'breed': selected_dog.dog_breed_id,
        'age': selected_dog.dog_age,
        'weight': selected_dog.dog_weight,
        'image': selected_dog.dog_image,
        'avg_age': DogBreeds.objects.filter(breed_name=selected_dog.dog_breed_id)[0].breed_average_lifespan,
        'avg_weight': DogBreeds.objects.filter(breed_name=selected_dog.dog_breed_id)[0].breed_average_weight,
        'exercise_needs': DogBreeds.objects.filter(breed_name=selected_dog.dog_breed_id)[0].breed_daily_exercise_needs,
    }
    content = {
        'title': 'Dog Info',
        'dog': dog,
    }
    return render(request, 'dog_walker/dog_info.html', content)


@login_required
def display_route(request):
    points = []
    if request.method == 'POST':
        if request.POST.get('duration'):
            temp_dict = {
                'walking_route_name': request.POST.get('route_name'),
                'walking_route_start': request.POST.get('start_point'),
                'walking_route_middle_1':
                    request.POST.get('middle_point_1') if request.POST.get('middle_point_1') else None,
                'walking_route_middle_2':
                    request.POST.get('middle_point_2') if request.POST.get('middle_point_2') else None,
                'walking_route_middle_3':
                    request.POST.get('middle_point_3') if request.POST.get('middle_point_3') else None,
                'walking_route_end': request.POST.get('end_point'),
                'walking_route_duration': request.POST.get('duration'),
                'walking_route_type': 'Leisure',
                'user_id': User.objects.get_by_natural_key(request.user)
            }
            WalkingRoute.objects.create(**temp_dict)
            return redirect('dog_walker-view_map')

        points.append(PointOfInterests.objects.filter(name=request.POST.get('start_point'))[0].location)
        if request.POST.get('middle_point_1'):
            points.append(PointOfInterests.objects.filter(name=request.POST.get('middle_point_1'))[0].location)
        if request.POST.get('middle_point_2'):
            points.append(PointOfInterests.objects.filter(name=request.POST.get('middle_point_2'))[0].location)
        if request.POST.get('middle_point_3'):
            points.append(PointOfInterests.objects.filter(name=request.POST.get('middle_point_3'))[0].location)
        points.append(PointOfInterests.objects.filter(name=request.POST.get('end_point'))[0].location)
    content = {
        'title': 'Display Route',
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


@login_required
def record_a_walk(request):
    return render(request, 'dog_walker/record_a_walk.html', {'title': 'Record A Walk'})


@login_required
def record_a_walk_own_info(request):
    current_user = request.user
    dog_list = Dogs.objects.filter(user_id=current_user)
    dogs = []
    for dog in dog_list:
        dogs.append(dog.dog_name)
    content = {
        'title': 'Record A Walk',
        'dogs': dogs,
    }
    return render(request, 'dog_walker/record_a_walk_own_info.html', content)


@login_required
def record_a_walk_saved_walking_route(request):
    current_user = request.user
    dog_list = Dogs.objects.filter(user_id=current_user)
    dogs = []
    for dog in dog_list:
        dogs.append(dog.dog_name)
    content = {
        'title': 'Record A Walk',
        'dogs': dogs,
    }
    return render(request, 'dog_walker/record_a_walk_saved_walking_route.html', content)

@login_required
def walking_classes(request):
    return render(request, 'dog_walker/walking_classes.html', {'title': 'Join A Class'})


@login_required
def dog_trainer_my_classes(request):
    return render(request, 'dog_walker/my_classes.html', {'title': 'My Classes'})


@login_required
def view_class_detail_dog_trainer(request):
    return render(request, 'dog_walker/view_class_detail_dog_trainer.html', {'title': 'Dog Trainer Class'})

@login_required
def view_class_detail_dog_walker(request):
    return render(request, 'dog_walker/view_class_detail_dog_walker.html', {'title': 'Dog Walker Class'})

@login_required
def dog_trainer_create_a_class(request):
    if request.method == 'POST':
        walking_Class_Subjects.walking_classes.append(
            None
            # TODO Add walking class object
        )
        walking_Class_Subjects.notify()
    return render(request, 'dog_walker/create_walking_class.html', {'title': 'Create A Class'})