from django.shortcuts import render


def home(request):
    return render(request, "homepage.html")


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "homepage/profile.html", {'username': username})
