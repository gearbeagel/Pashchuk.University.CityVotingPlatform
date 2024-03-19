from django.urls import path
from . import views

urlpatterns = [
    path('', views.overall_info, name='overall_info'),
    path('<int:project_id>/', views.detail, name='detail'),
    path('<int:project_id>/results/', views.results, name='results'),
    path('<int:project_id>/vote/', views.vote, name='vote'),
]
