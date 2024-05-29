from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from city_voting_registration.views import send_email
from help_and_support.forms import RequestTicketForm


def help_page(request):
    return render(request, 'help_and_support/FAQ.html')


@login_required
def submit_ticket(request):
    if request.method == "POST":
        form = RequestTicketForm(request.POST)
        if form.is_valid():
            user = request.user
            submission = form.save(commit=False)
            submission.user = request.user
            subject = 'Thanks for sharing a problem!'
            message = f'Dear {user.username}. Thank you for sharing a problem! Answer will be sent on this email in the nearest future.'
            send_email(request, subject, message)
            submission.save()
            messages.success(request, 'Your request ticket has been saved successfully.')
            return redirect('home')
    else:
        form = RequestTicketForm()
    return render(request, 'help_and_support/request_ticket.html', {'form': form})
