from io import BytesIO

import requests
from django.core.files import File
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from pitch_deck_generator.decks.models import (
    PdfToPPTXStorage,
    PitchDeck,
    QuestionAnswer,
)
from pitch_deck_generator.decks.tasks import (
    ML_HOST,
    create_images_mokups,
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
        elif instance.question.inner_tag == "names":
            instance.deck.name = instance.answer if instance.answer else None
            instance.deck.save()
        elif instance.question.inner_tag in ["finance_model"]:
            qenerate_answer_qr.apply_async(kwargs={"pk": instance.pk}, countdown=5)
        elif instance.question.inner_tag == "images":
            create_images_mokups.apply_async(kwargs={"pk": instance.pk}, countdown=5)
        save_answer_to_deck.apply_async(kwargs={"pk": instance.pk}, countdown=10)


@receiver(pre_save, sender=QuestionAnswer)
def question_answer_update(sender, instance: QuestionAnswer, **kwargs):
    if instance.id:
        if instance.question.inner_tag == "category":
            generate_numeric_values.apply_async(
                kwargs={"pk": instance.deck.pk}, countdown=1
            )
        elif instance.question.inner_tag == "names":
            instance.deck.name = instance.answer if instance.answer else None
            instance.deck.save()
        elif instance.question.inner_tag in ["finance_model"]:
            qenerate_answer_qr.apply_async(kwargs={"pk": instance.pk}, countdown=5)
        elif instance.question.inner_tag == "images":
            create_images_mokups.apply_async(kwargs={"pk": instance.pk}, countdown=5)
        save_answer_to_deck.apply_async(kwargs={"pk": instance.pk}, countdown=10)


@receiver(post_save, sender=PdfToPPTXStorage)
def pdt_to_pptx_convert(sender, instance: PdfToPPTXStorage, created, **kwargs):
    if created:
        with open(instance.pdf.path, "rb") as f:
            r = requests.post(ML_HOST + "convert-to-pptx", files={"in_file": f}).json()
            data = requests.get(ML_HOST + r["file"][1:]).content
            instance.pptx.save(
                instance.pdf.path.split("/")[-1].replace("pdf", "pptx"),
                File(
                    BytesIO(data),
                    instance.pdf.path.split("/")[-1].replace("pdf", "pptx"),
                ),
            )
        instance.save()
