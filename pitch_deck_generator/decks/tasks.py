from celery import shared_task

from ml.openai_handle import create_name_hint, create_hints
from pitch_deck_generator.decks.models import PitchDeck, Question, QuestionDeckHint


@shared_task
def run_pitch_deck_calculation(pk: int):
    generate_pitch_deck_name.apply_async(kwargs={"pk": pk})
    for i in range(3):
        generate_pitch_deck_name.apply_async(kwargs={"pk": pk, "num": pk})


@shared_task
def generate_pitch_deck_name(pk: int):
    pitch_deck = PitchDeck.objects.get(pk=pk)
    data = create_name_hint(pitch_deck.description)
    question = Question.objects.get(inner_tag=data["type"])
    QuestionDeckHint.objects.create(
        question=question,
        deck=pitch_deck,
        hint={"type": "text_array", "value": data["value"]},
    )


@shared_task
def generate_batch_hints(pk: int, num: int):
    pitch_deck = PitchDeck.objects.get(pk=pk)
    data = create_hints(pitch_deck.description, num)
    print(data)
