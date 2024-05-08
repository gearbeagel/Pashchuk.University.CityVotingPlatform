from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from city_voting_registration.views import send_email
from user_submissions.views import is_staff
from voting.models import Project, Comment
from .models import ReportOnComment, ReportOnProject


@login_required
@user_passes_test(is_staff, login_url='/')
def admin_panel(request):
    context = {}
    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            context['error_message'] = message.message
        elif message.level == messages.SUCCESS:
            context['success_message'] = message.message
    return render(request, 'admin_panel/admin_panel.html', context)


@login_required
def report_project(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    report = ReportOnProject.objects.filter(project=project, reported_by=request.user)
    if report:
        messages.error(request, 'You have already reported this project')
        return redirect('home')
    report = ReportOnProject.objects.create(project=project, reported_by=request.user)
    report.save()
    subject = f'Fate of {project.name} project'
    message = (f'Dear {project.user.username}. '
               ' Your project has been reported. It will still be visible until admins verdict')
    user_email = project.user.email
    send_email(request, subject, message, user_email)
    messages.success(request, 'Project was reported successfully. Wait for administration to response')
    return redirect('home')


@login_required
def report_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id).first()
    report = ReportOnComment.objects.filter(comment=comment, reported_by=request.user)
    if report:
        messages.error(request, 'You have already reported this comment')
        return redirect('home')
    report = ReportOnComment.objects.create(comment=comment, reported_by=request.user)
    report.save()
    subject = f'About your comment under {comment.project.name}'
    message = (f'Dear {comment.user.username}. '
               f' Your comment "{comment.comment_text}" has been reported. It will still be visible until admins verdict')
    user_email = comment.user.email
    send_email(request, subject, message, user_email)
    messages.success(request, 'Comment was reported successfully. Wait for administration to response')
    return redirect('home')


@login_required
@user_passes_test(is_staff, login_url='/')
def show_reported_projects(request):
    reports = ReportOnProject.objects.all()
    reports = reports.order_by('-id')
    reported_projects = []
    for report in reports:
        reported_projects.append(report.project)
    context = {'reported_projects': reported_projects}
    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            context['error_message'] = message.message
        elif message.level == messages.SUCCESS:
            context['success_message'] = message.message
    return render(request, "admin_panel/reported_projects.html", context)


@login_required
@user_passes_test(is_staff, login_url='/')
def show_reported_comments(request):
    reports = ReportOnComment.objects.all()
    reports = reports.order_by('-id')
    reported_comments = []
    for report in reports:
        reported_comments.append(report.comment)
    context = {'reported_comments': reported_comments}
    for message in messages.get_messages(request):
        if message.level == messages.ERROR:
            context['error_message'] = message.message
        elif message.level == messages.SUCCESS:
            context['success_message'] = message.message
    return render(request, "admin_panel/reported_comments.html", context)


@login_required
@user_passes_test(is_staff, login_url='/')
def reported_project_management(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            subject = 'Your project was deleted!'
            message = f'Dear {project.user.username}. Your project, {project.name}, was deleted due to a report.'
            user_email = project.user.email
            send_email(request, subject, message, user_email)
            reports = ReportOnProject.objects.filter(project=project).all()
            for report in reports:
                subject = 'Your report was accepted!'
                message = f'Dear {report.reported_by.username}. Your report on project {project.name} was approved and this project was deleted.'
                user_email = report.reported_by.email
                send_email(request, subject, message, user_email)
            reports.delete()
            project.delete()
            messages.success(request, 'Project was deleted.')
            return redirect('reported_projects')
        if action == 'reject':
            subject = 'Your project is no longer reported!'
            message = f'Dear {project.user.username}. Your project, {project.name}, is no longer reported.'
            user_email = project.user.email
            send_email(request, subject, message, user_email)
            reports = ReportOnProject.objects.filter(project=project).all()
            for report in reports:
                subject = 'Your report was rejected!'
                message = f'Dear {report.reported_by.username}. Your report on project {project.name} was rejected and this project will not be removed from our platform.'
                user_email = report.reported_by.email
                send_email(request, subject, message, user_email)
            reports.delete()
            messages.success(request, 'Project is no longer reported')
            return redirect('reported_projects')
    else:
        return redirect('reported_projects')


@login_required
@user_passes_test(is_staff, login_url='/')
def reported_comment_management(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            subject = 'Your comment was deleted!'
            message = f'Dear {comment.user.username}. Your comment, {comment.comment_text}, was deleted due to a report.'
            user_email = comment.user.email
            send_email(request, subject, message, user_email)
            reports = ReportOnComment.objects.filter(comment=comment).all()
            for report in reports:
                subject = 'Your report was accepted!'
                message = f'Dear {report.reported_by.username}. Your report on comment {comment.comment_text} was approved and this comment was deleted.'
                user_email = report.reported_by.email
                send_email(request, subject, message, user_email)
            reports.delete()
            comment.delete()
            messages.success(request, 'Comment was deleted.')
            return redirect('reported_comments')
        if action == 'reject':
            subject = 'Your comment is no longer reported!'
            message = f'Dear {comment.user.username}. Your comment, {comment.comment_text}, is no longer reported.'
            user_email = comment.user.email
            send_email(request, subject, message, user_email)
            reports = ReportOnComment.objects.filter(comment=comment).all()
            for report in reports:
                subject = 'Your report was rejected!'
                message = f'Dear {report.reported_by.username}. Your report on comment {comment.comment_text} was rejected and this comment will not be removed from our platform.'
                user_email = report.reported_by.email
                send_email(request, subject, message, user_email)
            reports.delete()
            messages.success(request, 'Comment is no longer reported')
            return redirect('reported_comments')
    else:
        return redirect('reported_comments')
