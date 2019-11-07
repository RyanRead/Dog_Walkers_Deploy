from django.shortcuts import render
from .models import PointOfInterests, DogBreeds, Dogs
from django.core.serializers import serialize
from django.http import HttpResponse


def point_of_interest_dataset(request):
    points = []
    for point in PointOfInterests.objects.filter(is_private=False):
        points.append(point)
    for point in PointOfInterests.objects.filter(is_private=True, creator=request.user):
        points.append(point)
    data = serialize('geojson', points)
    return HttpResponse(data, content_type='json')




