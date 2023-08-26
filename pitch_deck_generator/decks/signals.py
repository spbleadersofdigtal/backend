from django.db.models.signals import post_save
from django.dispatch import receiver

from pitch_deck_generator.decks.models import PitchDeck, QuestionAnswer
from pitch_deck_generator.decks.tasks import (
    generate_numeric_values,
    run_pitch_deck_calculation,
)


@receiver(post_save, sender=PitchDeck)
def tag_create(sender, instance: PitchDeck, created, **kwargs):
    if created:
        run_pitch_deck_calculation.apply_async(kwargs={"pk": instance.pk})


@receiver(post_save, sender=QuestionAnswer)
def question_numeric_run(sender, instance: QuestionAnswer, created, **kwargs):
    if created:
        if instance.question.inner_tag == "category":
            generate_numeric_values.apply_async(kwargs={"pk": instance.deck.pk})
