from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from azure.storage.blob import BlobServiceClient
import os

from homepage.models import ImageStorage


@login_required
def welcome_email(request):
    user = request.user
    subject = 'Welcome to City Voting Platform!'
    message = f'{user.username}, thanks for becoming a part of our community!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect("home")


def delete_user(request):
    user = request.user
    azure_storage_connection_string = os.getenv("connection_str")
    container_name = "profpicscont"
    userpic = ImageStorage.objects.filter(user=request.user).first()
    blob_name = userpic.profile_picture
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.delete_blob()
    user.delete()
    return redirect('home')
