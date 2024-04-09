from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
]
