from django.db.models.signals import post_save
from django.dispatch import receiver

from pitch_deck_generator.decks.models import PitchDeck
from pitch_deck_generator.decks.tasks import run_pitch_deck_calculation


@receiver(post_save, sender=PitchDeck)
def tag_create(sender, instance: PitchDeck, created, **kwargs):
    if created:
        run_pitch_deck_calculation.apply_async(kwargs={"pk": instance.pk})
