from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ImageStorage
from .forms import ProfilePictureForm
from voting.models import Project


def home(request):
    projects = Project.objects.order_by('-pub_date')[:5]
    return render(request, "homepage/projects.html", {'projects': projects})


@login_required
def profile(request):
    profile_picture_object = ImageStorage.objects.filter(user=request.user).first()
    profile_picture = profile_picture_object.profile_picture if profile_picture_object else None

    context = {'profile_picture': profile_picture}

    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            context['error_message'] = message.message
        elif message.level == messages.SUCCESS:
            context['success_message'] = message.message

    return render(request, "homepage/profile.html", context)


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


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('new_profile_picture')
        if profile_picture:
            existing_image = ImageStorage.objects.filter(user=request.user).first()
            if existing_image:
                existing_image.profile_picture.delete()
                existing_image.profile_picture = profile_picture
                existing_image.save()
            else:
                ImageStorage.objects.create(user=request.user, profile_picture=profile_picture)
            messages.success(request, 'Profile picture has been changed.')
            return redirect('profile')
        else:
            messages.error(request, "No profile picture uploaded. Please choose a file.")
            return redirect('profile')
    else:
        form = ProfilePictureForm()
        return render(request, 'homepage/profile.html', {'form': form})
