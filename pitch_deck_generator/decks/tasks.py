import tempfile

import qrcode
import requests
from celery import shared_task
from django.core.files import File

from ml.openai_handle import create_hints, create_name_hint
from pitch_deck_generator.decks.models import (
    PitchDeck,
    Question,
    QuestionAnswer,
    QuestionAnswerPhoto,
    QuestionDeckHint,
)

ML_HOST = "https://short-peaches-speak.loca.lt/"

data_types = {
    "names": ("text", 1),
    "type": ("select", 13),
    "category": ("text", 14),
    "users": ("text", 2),
    "problems": ("text", 3),
    "actuality": ("text", 4),
    "solve": ("text", 5),
    "works": ("text", 6),
    "awards": ("text", 7),
    "market_values": ("multiple_range", 8),
    "percentage": ("multiple_range", 9),
    "project_stage": ("select", 10),
    "money": ("text", 11),
    "financial_indicators": ("text", 33),
    "users_metrics": ("multiple_range", 12),
    "aims": ("multiple_date_description", 15),
    "money_recieved": ("number", 16),
    "past_investors": ("text", 17),
    "how_much_investments": ("range", 18),
    "finance_model": ("link", 19),
    "company_value": ("range", 20),
    "investments_sold": ("text", 21),
    "time_to_spend": ("date", 22),
    "achieve": ("text", 23),
    "future_value": ("range", 24),
    "your_role": ("photo_description", 25),
    "your_teammates": ("multiple_photo_description", 26),
    "competitors": ("text", 27),
    "competitors_strength": ("text", 28),
    "competitors_low": ("text", 29),
    "advantages": ("text", 30),
    "images": ("multiple_photo", 31),
    "links": ("multiple_link_description", 32),
}


@shared_task
def run_pitch_deck_calculation(pk: int):
    generate_pitch_deck_name.apply_async(kwargs={"pk": pk})
    generate_known_values.apply_async(kwargs={"pk": pk})
    for i in range(3):
        generate_batch_hints.apply_async(kwargs={"pk": pk, "num": i}, delay=1)


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
def generate_known_values(pk: int):
    pitch_deck = PitchDeck.objects.get(pk=pk)
    req = requests.post(
        ML_HOST + "search",
        json={"body": pitch_deck.description},
    )
    data = req.json()
    _, question_id = data_types["competitors"]
    QuestionDeckHint.objects.create(
        question_id=question_id, deck=pitch_deck, hint={"type": "cards", "value": data}
    )


@shared_task
def generate_batch_hints(pk: int, num: int):
    pitch_deck = PitchDeck.objects.get(pk=pk)
    try:
        data = create_hints(pitch_deck.description, num)
    except Exception as e:
        print(e)
        data = create_hints(pitch_deck.description, num)
    for el in data:
        question_type, question_id = data_types[el["type"]]
        if el["type"] == "aims":
            dates = {}
            for e in el["value"]:
                dates[e["date"]] = e["aim"]
            QuestionDeckHint.objects.create(
                question_id=question_id,
                deck=pitch_deck,
                hint={"type": question_type, "value": dates},
            )
        else:
            QuestionDeckHint.objects.create(
                question_id=question_id,
                deck=pitch_deck,
                hint={"type": question_type, "value": el["value"]},
            )


@shared_task
def generate_numeric_values(pk: int):
    pitch_deck = PitchDeck.objects.get(pk=pk)
    if q := QuestionAnswer.objects.filter(
        question__inner_tag="category", deck=pitch_deck
    ):
        if q2 := QuestionAnswer.objects.filter(
            question__inner_tag="type", deck=pitch_deck
        ):
            category = q.first().answer
            type = q2.first().answer
            req = requests.post(
                ML_HOST + "numeric",
                json={
                    "description": pitch_deck.description,
                    "category": category,
                    "type": type,
                },
            )
            data = req.json()
            for el in data:
                question_type, question_id = data_types[el["type"]]
                QuestionDeckHint.objects.create(
                    question_id=question_id,
                    deck=pitch_deck,
                    hint={"type": question_type, "value": el["value"]},
                )


@shared_task
def save_answer_to_deck(pk: int):
    qa = QuestionAnswer.objects.get(pk=pk)
    question = qa.question
    deck = qa.deck
    deck.questions[question.inner_tag] = {
        "answer": qa.answer,
        "photos": [x.file.url for x in qa.photos.all()],
    }
    deck.save()


@shared_task
def qenerate_answer_qr(pk: int):
    qa = QuestionAnswer.objects.get(pk=pk)
    link = qa.answer
    img = qrcode.make(link)
    with tempfile.NamedTemporaryFile() as tmp:
        img.save(tmp.name)
        QuestionAnswerPhoto.objects.create(
            answer=qa,
            file=File(tmp, name="qr.png"),
        )
