from django.shortcuts import render

from voting.models import Project


def home(request):
    projects = Project.objects.order_by('-pub_date')[:5]
    return render(request, "homepage/homepage.html", {'projects': projects})


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "homepage/profile.html", {'username': username})
