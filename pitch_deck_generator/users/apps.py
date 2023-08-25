from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "pitch_deck_generator.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import pitch_deck_generator.users.signals  # noqa F401
        except ImportError:
            pass
