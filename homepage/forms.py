from django import forms
from storages.backends.azure_storage import AzureStorage

from .models import ImageStorage
from CityVotingPlatform import settings


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ImageStorage
        fields = ['profile_picture']

    def save(self, commit=True):
        instance = super().save(commit=False)
        profile_picture = self.cleaned_data.get('profile_picture')

        azure_storage = AzureStorage(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY,
        )

        instance.profile_picture = azure_storage.save(profile_picture.name, profile_picture)

        if commit:
            instance.save()
        return instance
