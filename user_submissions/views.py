from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import UserSubmissionForm
from .models import UserSubmission
from voting.models import Project
from django.contrib import messages


def is_staff(user):
    return user.is_staff


@login_required
def submit_proposal(request):
    if request.method == "POST":
        form = UserSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserSubmissionForm()
    return render(request, 'proposal_submission/proposal_form.html', {'form': form})


@login_required
@user_passes_test(is_staff, login_url='/')
def approve_proposal(request, project_id):
    submission = UserSubmission.objects.get(pk=project_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            project = Project(name=submission.name,
                              description=submission.description,
                              district=submission.district
                              )
            submission.is_approved = True
            project.save()
            submission.delete()
            messages.success(request, 'Proposal was approved.')
            return redirect('proposals')
        if action == 'reject':
            submission.delete()
            messages.error(request, 'Proposal was rejected.')
            return redirect('proposals')
    else:
        return redirect('proposals')


@login_required
@user_passes_test(is_staff, login_url='/')
def proposals(request):
    proposal_projects = UserSubmission.objects.order_by('-id')
    fail_message = None
    success_message = None

    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            fail_message = message.message
        elif message.level == messages.SUCCESS:
            success_message = message.message

    return render(request, "proposal_submission/propose_approval.html", {
        'proposal_projects': proposal_projects,
        'fail_message': fail_message,
        'success_message': success_message
    })
