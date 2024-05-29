from django import forms
from .models import RequestTicket


class RequestTicketForm(forms.ModelForm):
    class Meta:
        model = RequestTicket
        fields = ['id', 'title', 'description']
