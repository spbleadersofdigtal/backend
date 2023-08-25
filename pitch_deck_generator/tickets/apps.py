from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pitch_deck_generator.tickets"

    def ready(self):
        try:
            import pitch_deck_generator.tickets.signals  # noqa F401
        except ImportError:
            pass
