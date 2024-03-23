from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.detail, name='detail'),
    path('<int:project_id>/vote/', views.vote, name='vote'),
]
