from django.shortcuts import render
from .models import LatLngPins, DogBreeds, Dogs
from django.core.serializers import serialize
from django.http import HttpResponse


def point_of_interest_dataset(request):
    data = serialize('geojson', LatLngPins.objects.all())
    return HttpResponse(data, content_type='json')


def dog_breed_dataset(request):
    data = DogBreeds.objects.all()
    return HttpResponse(data, content_type='json')


def dogs_dataset(request):
    data = Dogs.objects.all()
    return HttpResponse(data, content_type='json')




