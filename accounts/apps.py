from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Danh Sách Tài Khoản Game'

    def ready(self):
        import accounts.signals