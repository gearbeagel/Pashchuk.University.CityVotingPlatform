from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def city_map(request):
    return render(request, 'citymap/city_map.html')
