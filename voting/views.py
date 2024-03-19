from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Project, Vote, UserChoice


# Get project's info and display it
def overall_info(request):
    latest_project_list = Project.objects.order_by('-pub_date')[:4]
    context = {'latest_project_list': latest_project_list}
    return render(request, 'voting/overall_info.html', context)


# Show specific project data and votes
def detail(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'city_voting/detail.html', {'project': project})


# Get project data and display results
def results(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'city_voting/results.html', {'project': project})


# Vote for a project
@login_required
def vote(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if UserChoice.objects.filter(user=user, project=project).exists():
        return render(request, 'city_voting/detail.html',
                      {'project': project, 'error_message': 'You have already voted for this project.'})
    try:
        selected_choice = project.vote_set.get(pk=request.POST['vote'])
    except (KeyError, Vote.DoesNotExist):
        return render(request, 'city_voting/detail.html',
                      {'project': project,
                       'error_message': 'You did not select a choice.'})
    else:
        UserChoice.objects.create(user=user, project=project, vote=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(project.id,)))
