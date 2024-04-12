from django.shortcuts import render


def city_map(request):
    return render(request, 'citymap/city_map.html')
