from django import forms


class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()
