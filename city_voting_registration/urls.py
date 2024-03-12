from django.urls import path
from . import views

urlpatterns = [
    path('sing_up/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('sing_in/', views.login_view, name='login'),
]
