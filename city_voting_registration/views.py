from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.


# Create your views here.
def home(request):
    return render(request, "homepage.html")


def register(request):
    return render(request, "register.html")


def callback_view(request):
    return redirect(reverse('home'))


def profile(request):
    return render(request, "profile.html")
