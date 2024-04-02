from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from voting.models import Project


def home(request):
    projects = Project.objects.order_by('-pub_date')[:5]
    return render(request, "homepage/projects.html", {'projects': projects})


@login_required
def profile(request):
    error_message = None
    success_message = None
    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            error_message = message.message
            return render(request, "homepage/profile.html", {'error_message': error_message})
        elif message.level == messages.SUCCESS:
            success_message = message.message
            return render(request, "homepage/profile.html", {'success_message': success_message})
    return render(request, "homepage/profile.html")


@login_required
def update_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username has been changed.')
            return redirect('profile')
        else:
            messages.error(request, 'Username cannot be empty.')
            return redirect('profile')
    return redirect('profile')
