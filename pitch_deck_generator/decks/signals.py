from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from pitch_deck_generator.decks.models import PitchDeck, QuestionAnswer
from pitch_deck_generator.decks.tasks import (
    generate_numeric_values,
    qenerate_answer_qr,
    run_pitch_deck_calculation,
    save_answer_to_deck,
)


@receiver(post_save, sender=PitchDeck)
def pitch_deck_create(sender, instance: PitchDeck, created, **kwargs):
    if created:
        run_pitch_deck_calculation.apply_async(kwargs={"pk": instance.pk}, delay=1)


@receiver(post_save, sender=QuestionAnswer)
def question_answer_create(sender, instance: QuestionAnswer, created, **kwargs):
    if created:
        if instance.question.inner_tag == "category":
            generate_numeric_values.apply_async(
                kwargs={"pk": instance.deck.pk}, countdown=1
            )
        elif instance.question.inner_tag in ["finance_model"]:
            qenerate_answer_qr.apply_async(kwargs={"pk": instance.pk}, countdown=1)
        save_answer_to_deck.apply_async(kwargs={"pk": instance.pk}, countdown=5)


@receiver(pre_save, sender=QuestionAnswer)
def question_answer_update(sender, instance: QuestionAnswer, created, **kwargs):
    if instance.id:
        if instance.question.inner_tag == "category":
            generate_numeric_values.apply_async(
                kwargs={"pk": instance.deck.pk}, countdown=1
            )
        elif instance.question.inner_tag in ["finance_model"]:
            qenerate_answer_qr.apply_async(kwargs={"pk": instance.pk}, countdown=1)
        save_answer_to_deck.apply_async(kwargs={"pk": instance.pk}, countdown=5)
