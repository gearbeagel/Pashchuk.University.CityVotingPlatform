from django.urls import path

from . import views
urlpatterns = [
    path('help/', views.help_page, name='help_page'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
]