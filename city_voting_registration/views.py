from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    return render(request, "homepage.html")


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            subject = 'Welcome to City Voting Platform!'
            message = f'{username}, thanks for becoming a part of our community!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "profile.html", {'username': username})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect("login")
