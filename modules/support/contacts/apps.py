from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.support.contacts'

    def ready(self):
        import modules.support.contacts.signals

