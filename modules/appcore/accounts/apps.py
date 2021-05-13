from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.appcore.accounts'

    def ready(self):
       import modules.appcore.accounts.signals
    


  