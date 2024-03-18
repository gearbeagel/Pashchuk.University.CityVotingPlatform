from django.shortcuts import render


# Create your views here.
def city_map(request):
    return render(request, 'citymap/city_map.html')
