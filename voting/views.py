from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Project, Vote, UserChoice


# Show specific project data and votes
def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    user_voted = UserChoice.objects.filter(user=user, project=project)
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    if user_voted:
        return render(request, 'voting/detail.html', {'project': project, 'user_voted': user_voted})
    else:
        return render(request, 'voting/detail.html', {'project': project})


# Vote for a project
@login_required
def vote(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    user_voted = UserChoice.objects.filter(user=user, project=project)
    if user_voted.exists():
        return render(request, 'voting/detail.html',
                      {'project': project, 'user_voted': user_voted})
    try:
        selected_choice = project.vote_set.get(pk=request.POST['vote'])
    except (KeyError, Vote.DoesNotExist):
        return render(request, 'voting/detail.html',
                      {'project': project,
                       'error_message': 'You did not select a choice.'})
    else:
        UserChoice.objects.create(user=user, project=project, vote=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        success_message = 'Your vote has been recorded successfully.'
        return render(request, 'voting/detail.html',
                      {'project': project, 'success_message': success_message, 'user_voted': user_voted})
