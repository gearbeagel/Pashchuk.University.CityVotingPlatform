from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from voting.models import Project


@login_required(login_url='/')
def city_map(request):
    return render(request, 'citymap/city_map.html')


@login_required(login_url='/')
def get_projects_by_district(request):
    if request.method == 'GET':
        district_name = request.GET.get('district')
        if district_name:
            projects = Project.objects.filter(district=district_name)[:5]
            data = [{'name': project.name, 'description': project.description, 'id': project.id} for project in projects]
            return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)
