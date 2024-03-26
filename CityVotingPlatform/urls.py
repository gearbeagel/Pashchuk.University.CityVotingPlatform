from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("allauth.urls")),
    path('', include('city_voting_registration.urls')),
    path('', include('city_map.urls')),
    path('', include('homepage.urls')),
    path('projects/', include('voting.urls')),
    path('proposal/', include('user_submissions.urls')),
]
