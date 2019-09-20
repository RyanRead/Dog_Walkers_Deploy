from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'map/home.html', {'title': 'Home'})


def view_map(request):
    return render(request, 'map/view_map.html', {'title': 'View Map'})
