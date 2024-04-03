from azure.storage.blob import BlobServiceClient
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os

from .models import ImageStorage
from .forms import ProfilePictureForm
from voting.models import Project


def home(request):
    projects = Project.objects.order_by('-pub_date')[:5]
    return render(request, "homepage/projects.html", {'projects': projects})


@login_required
def profile(request):
    azure_storage_connection_string = os.getenv("connection_str")
    container_name = "profpicscont"
    userpic = ImageStorage.objects.filter(user=request.user).first()
    if not userpic:
        userpic = ImageStorage.objects.create(user=request.user)
        userpic.save()
    blob_name = userpic.profile_picture

    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    profile_picture = blob_client.url
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
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.container_name = 'profpicscont'
            profile_picture = form.cleaned_data['profile_picture']
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
            messages.error(request, 'Error updating profile picture. Please try again.')
            return redirect('profile')
    else:
        return redirect('profile')

