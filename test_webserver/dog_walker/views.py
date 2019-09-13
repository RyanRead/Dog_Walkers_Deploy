from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author' : 'Me',
        'title' : 'Hello Friends',
        'content': 'Stuffffffff',
        'date_posted' : 'August 19, 2099'
    },
    {
        'author': 'You',
        'title': 'Hello Enemies',
        'content': 'Stufffffdsffff',
        'date_posted': 'August 19, 2089'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'dog_walker/home.html', context)

def about(request):
    return render(request, 'dog_walker/about.html', {'title': 'about'})


