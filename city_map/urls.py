from django.urls import path
from city_map import views

urlpatterns = [
    path('city_map/', views.city_map, name='city_map'),
    path('projects/', views.get_projects_by_district, name='get_projects_by_district'),
]
