from django.apps import AppConfig


class CityVotingRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_voting_registration'

    def ready(self):
        import city_voting_registration.signals
