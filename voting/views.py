from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages

from .models import Project, Vote, UserChoice, Comment
from homepage.models import ImageStorage


# Show specific project data and votes
def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    user_voted = UserChoice.objects.filter(user=user, project=project)
    comments = Comment.objects.filter(project=project)
    comments = comments.order_by('-pub_date')
    img_object = ImageStorage.objects.filter(user=user).first()
    profile_picture = None
    if img_object:
        profile_picture = img_object.profile_picture
    error_message = None
    success_message = None
    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            error_message = message.message
        elif message.level == messages.SUCCESS:
            success_message = message.message
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    if user_voted:
        if error_message:
            return render(request, 'voting/detail.html',
                          {'project': project, 'user_voted': user_voted, 'comments': comments,
                           'error_message': error_message, 'profile_picture': profile_picture})
        elif success_message:
            return render(request, 'voting/detail.html',
                          {'project': project, 'user_voted': user_voted, 'comments': comments,
                           'success_message': success_message, 'profile_picture': profile_picture})
        else:
            return render(request, 'voting/detail.html',
                          {'project': project, 'user_voted': user_voted, 'comments': comments, 'profile_picture': profile_picture})
    else:
        if error_message:
            return render(request, 'voting/detail.html',
                          {'project': project, 'user_voted': user_voted, 'comments': comments,
                           'error_message': error_message, 'profile_picture': profile_picture})
        else:
            return render(request, 'voting/detail.html',
                          {'project': project, 'comments': comments, 'profile_picture': profile_picture})


# Vote for a project
@login_required
def vote(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    user_voted = UserChoice.objects.filter(user=user, project=project)
    if user_voted.exists():
        return redirect('detail', project_id=project_id)
    try:
        selected_choice = project.vote_set.get(pk=request.POST['vote'])
    except (KeyError, Vote.DoesNotExist):
        messages.error(request, 'You did not select a choice')
        return redirect('detail', project_id=project_id)
    else:
        UserChoice.objects.create(user=user, project=project, vote=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, 'Your vote has been recorded successfully.')
        return redirect('detail', project_id=project_id)


# Add comment to a project
@login_required
def add_comment(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        comment_text = request.POST.get('comment_text')
        user_voted = UserChoice.objects.filter(user=request.user, project=project)
        if user_voted:
            if comment_text and user_voted:
                comment = Comment.objects.create(project=project, user=request.user, comment_text=comment_text)
                comment.save()
                messages.success(request, 'Thanks for commenting!')
                return redirect('detail', project_id=project_id)
            else:
                messages.error(request, 'Comment cannot be empty.')
                return redirect('detail', project_id=project_id)
        else:
            messages.error(request, 'Vote to leave a comment.')
            return redirect('detail', project_id=project_id)
    else:
        return redirect('detail', project_id=project_id)
