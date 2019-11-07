from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, IsTrainerForm
from django.contrib.auth.decorators import login_required
from .observer_pattern import ConcreteObserver, ConcreteSubject
from .factory_method import *
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta


success_factory = ConcreteSuccessMessageCreator()
error_factory = ConcreteErrorMessageCreator()

walking_class_subjects = ConcreteSubject()
users = User.objects.all()

for my_user in users:
    walking_class_subjects.register(ConcreteObserver(my_user.username, my_user.email))


@login_required
def home(request):
    # TODO Add user to list if their not in the list
    return render(request, 'dog_walker/home.html')


@login_required
def dog_trainer_home(request):
    return render(request, 'dog_walker/dog_trainer_home.html', {'title': 'Dog Trainer Home'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        is_trainer_form = IsTrainerForm(request.POST)
        if user_form.is_valid() and is_trainer_form.is_valid():
            user_form.save()
            new_user_name = user_form.cleaned_data.get('username')
            is_t = is_trainer_form.cleaned_data.get('is_trainer')
            profiles = Profile.objects.all()
            for profile in profiles:
                if profile.user.username == new_user_name:
                    profile.is_trainer = is_t
                    profile.save()
        return redirect('dog_walker-login')
    else:
        user_form = UserRegistrationForm()
        is_trainer_form = IsTrainerForm()

    content = {
        'title': 'Register',
        'user_form': user_form,
        'is_trainer_form': is_trainer_form
    }
    return render(request, 'dog_walker/register.html', content)


@login_required
def view_map(request):
    print(request.user)
    return render(request, 'dog_walker/view_map.html', {'title': 'View Map'})


@login_required
def add_a_dog(request):
    if request.method == 'POST':
        age = 2019 - int(request.POST.get('dog_birthday')[:4])
        if request.FILES['dog_image'].name is not None:
            dog_image = request.FILES['dog_image']
            dog_image_name = dog_image.name
            save_file = FileSystemStorage()
            save_file.save(dog_image_name, dog_image)
        else:
            messages.error(request, error_factory.createProduct("not_image").get_message())
            dog_image_name = 'default.png'
            return redirect('dog_walker-add_a_dog')

        temp_dict = {
            'user_id': User.objects.get_by_natural_key(request.user),
            'dog_name': request.POST.get('dog_name').capitalize(),
            'dog_breed_id': DogBreeds.objects.get(breed_name=request.POST.get('dog_breed')),
            'dog_age': age,
            'dog_weight': request.POST.get('dog_weight'),
            'dog_image': '/static/dogs/' + dog_image_name
        }
        Dogs.objects.create(**temp_dict)
        messages.success(request, success_factory.createProduct("add_dog").get_message())
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
        if not (request.POST.get('lng') and request.POST.get('lat')):
            messages.error(request, error_factory.createProduct("add_poi").get_message())
        else:
            PointOfInterests.objects.create(**temp_dict)
            messages.success(request, success_factory.createProduct("add_poi").get_message())
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
    dates = []
    exercise_today = 0
    for i in range(7):
        temp_date = date.today() - timedelta(days=i)
        total_exercise = 0
        for exercise in RecordedExercise.objects.filter(dog_id=selected_dog, exercise_date=temp_date):
            total_exercise += exercise.exercise_duration
        if i == 0:
            exercise_today = total_exercise
        day_info = {
            'date': temp_date,
            'exercise': total_exercise
        }
        dates.append(day_info)
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
        'dates': dates,
        'exercise_today': exercise_today,
    }
    return render(request, 'dog_walker/dog_info.html', content)


@login_required
def display_route(request):
    points = []
    if request.method == 'POST':
        if request.POST.get('duration'):
            temp_dict = {
                'walking_route_name': request.POST.get('route_name'),
                'walking_route_start': PointOfInterests.objects.filter(id=request.POST.get('start_point'))[0],
                'walking_route_middle_1':
                    PointOfInterests.objects.filter(id=request.POST.get('middle_point_1')) if request.POST.get('middle_point_1') else None,
                'walking_route_middle_2':
                    PointOfInterests.objects.filter(id=request.POST.get('middle_point_2')) if request.POST.get('middle_point_2') else None,
                'walking_route_middle_3':
                    PointOfInterests.objects.filter(id=request.POST.get('middle_point_3')) if request.POST.get('middle_point_3') else None,
                'walking_route_end': PointOfInterests.objects.filter(id=request.POST.get('end_point'))[0],
                'walking_route_duration': request.POST.get('duration'),
                'walking_route_type': 'Leisure', #TODO Add both
                'user_id': User.objects.get_by_natural_key(request.user)
            }
            WalkingRoute.objects.create(**temp_dict)
            messages.success(request, success_factory.createProduct("save_leisure_route").get_message())
            return redirect('dog_walker-view_map')

        start_point = PointOfInterests.objects.filter(name=request.POST.get('start_point'))[0]
        end_point = PointOfInterests.objects.filter(name=request.POST.get('end_point'))[0]

        points.append(start_point)
        if request.POST.get('middle_point_1'):
            middle_point_1 = PointOfInterests.objects.filter(name=request.POST.get('middle_point_1'))[0]
            points.append(middle_point_1)
        if request.POST.get('middle_point_2'):
            middle_point_2 = PointOfInterests.objects.filter(name=request.POST.get('middle_point_2'))[0]
            points.append(middle_point_2)
        if request.POST.get('middle_point_3'):
            middle_point_3 = PointOfInterests.objects.filter(name=request.POST.get('middle_point_3'))[0]
            points.append(middle_point_3)
        points.append(end_point)

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
    if request.method == 'POST':
        start = request.POST.get('walk_start')
        end = request.POST.get('walk_end')
        duration = (int(end[-2:]) - int(start[-2:])) + ((int(end[:2]) - int(start[:2])) * 60)
        duration = duration + 720 if duration < 0 else duration
        recorded_exercise = {
            'dog_id': Dogs.objects.filter(user_id=current_user, dog_name=request.POST.get('dog_name'))[0],
            'exercise_date': request.POST.get('walk_date'),
            'exercise_duration': duration,
        }
        RecordedExercise.objects.create(**recorded_exercise)
        messages.success(request, success_factory.createProduct("save_exercise").get_message())
        return redirect('dog_walker-my_dogs_homepage')

    dog_list = Dogs.objects.filter(user_id=current_user)
    route_list = WalkingRoute.objects.all()
    dogs = []
    routes = []

    for dog in dog_list:
        dogs.append(dog.dog_name)
    for route in route_list:
        routes.append(route.walking_route_name)
    content = {
        'title': 'Record A Walk',
        'dogs': dogs,
        'routes': routes,
    }
    return render(request, 'dog_walker/record_a_walk_saved_walking_route.html', content)


@login_required
def walking_classes(request):
    # TODO Dont display the button if registered or full
    current_user = request.user
    if request.method == 'POST':
        class_object = WalkingClass.objects.filter(id=request.POST.get('class_id'))[0]
        join_class = {
            'user_id': current_user,
            'class_id': class_object
        }
        if class_object.class_participants < class_object.class_max_participants:
            class_object.class_participants += 1
            class_object.save()
            JoinedClass.objects.create(**join_class)
            messages.success(request, success_factory.createProduct("join_walking_class").get_message())
        else:
            messages.error(request, error_factory.createProduct("full_class").get_message())

    classes = WalkingClass.objects.all()
    content = {
        'title': 'Join A Class',
        'classes': classes
    }
    return render(request, 'dog_walker/walking_classes.html', content)


@login_required
def dog_trainer_my_classes(request):
    current_user = request.user
    class_list = WalkingClass.objects.filter(class_instructor=current_user)
    classes = []
    for class_object in class_list:
        classes.append(class_object)

    content = {
        'title': 'My Classes',
        'classes': classes,
    }
    return render(request, 'dog_walker/my_classes.html', content)


@login_required
def view_class_detail_dog_trainer(request, class_name):
    current_user = request.user
    class_object = WalkingClass.objects.filter(class_instructor=current_user, class_name=class_name)[0]
    route_object = class_object.walking_route_id

    points = []
    points.append(route_object.walking_route_start.location)
    if route_object.walking_route_middle_1:
        points.append(route_object.walking_route_middle_1.location)
    if route_object.walking_route_middle_2:
        points.append(route_object.walking_route_middle_2.location)
    if route_object.walking_route_middle_3:
        points.append(route_object.walking_route_middle_3.location)
    points.append(route_object.walking_route_end.location)
    print(points)
    content = {
        'title': 'Dog Trainer Class',
        'class': class_object,
        'points': points
    }
    return render(request, 'dog_walker/view_class_detail_dog_trainer.html', content)


@login_required
def view_class_detail_dog_walker(request, instructor, class_name):
    instructor = User.objects.get_by_natural_key(instructor)
    class_object = WalkingClass.objects.filter(class_instructor=instructor, class_name=class_name)[0]
    route_object = class_object.walking_route_id

    points = []
    points.append(route_object.walking_route_start.location)
    if route_object.walking_route_middle_1:
        points.append(route_object.walking_route_middle_1.location)
    if route_object.walking_route_middle_2:
        points.append(route_object.walking_route_middle_2.location)
    if route_object.walking_route_middle_3:
        points.append(route_object.walking_route_middle_3.location)
    points.append(route_object.walking_route_end.location)
    print(points)
    content = {
        'title': 'Dog Trainer Class',
        'class': class_object,
        'points': points
    }
    return render(request, 'dog_walker/view_class_detail_dog_walker.html', content)


@login_required
def dog_trainer_create_a_class(request):
    current_user = request.user
    if request.method == 'POST':
        print(request.POST.get('class_name'))
        class_dict = {
            'class_name': request.POST.get('class_name'),
            'class_instructor': current_user,
            'walking_route_id': WalkingRoute.objects.filter(walking_route_name=request.POST.get('class_route'))[0],
            'class_date': request.POST.get('class_date'),
            'class_time': request.POST.get('class_date') + ' ' + request.POST.get('class_start'),
            'class_max_participants': request.POST.get('class_participants'),
            'class_full': False,
            'class_description': request.POST.get('class_description')
        }
        WalkingClass.objects.create(**class_dict)
        messages.success(request, success_factory.createProduct("save_walking_class").get_message())
        walking_class_subjects.walking_classes.append(
            WalkingClass.objects.filter(class_name=class_dict['class_name'])[0]
        )
        walking_class_subjects.notify()
        return redirect('dog_trainer-home')

    route_list = WalkingRoute.objects.all()
    routes = []
    for route in route_list:
        routes.append(route.walking_route_name)

    content = {
        'title': 'Create A Class',
        'routes': routes
    }
    return render(request, 'dog_walker/create_walking_class.html', content)
