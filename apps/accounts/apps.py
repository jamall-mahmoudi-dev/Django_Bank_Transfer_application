from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'  # این باید 'apps.accounts' باشد
    label = 'accounts'  # این خط مهم است