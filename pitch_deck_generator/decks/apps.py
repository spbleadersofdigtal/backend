from django.apps import AppConfig


class DecksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pitch_deck_generator.decks"

    def ready(self):
        try:
            import pitch_deck_generator.decks.signals  # noqa F401
        except ImportError:
            pass
