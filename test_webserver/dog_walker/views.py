from django.shortcuts import render
from .models import LatLngPins
from django.core.serializers import serialize
from django.http import HttpResponse
import json


def home(request):
    return render(request, 'dog_walker/home.html')


def about(request):
    return render(request, 'dog_walker/about.html', {'title': 'About'})


def view_map(request):
    return render(request, 'dog_walker/view_map.html', {'title': 'View Map'})


def point_of_interest_datasets(request):
    data = serialize('geojson', LatLngPins.objects.all())
    return HttpResponse(data, content_type='json')




def my_dogs_homepage(request):
    return render(request, 'dog_walker/my_dogs_homepage.html', {'title': 'My Dogs'})


def dog_info(request):
    return render(request, 'dog_walker/dog_info.html', {'title': 'Dog Info'})



