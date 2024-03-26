from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_proposal, name='submit_proposal'),
    path('approval/', views.proposals, name='proposals'),
    path('approval/<int:project_id>', views.approve_proposal, name='approve_proposal'),
]
