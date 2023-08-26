import requests
from celery import shared_task

from ml.openai_handle import create_name_hint, create_hints
from pitch_deck_generator.decks.models import PitchDeck, Question, QuestionDeckHint

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
    "aims": ("text", 15),
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
        generate_batch_hints.apply_async(kwargs={"pk": pk, "num": i})


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
    _, question_id = data_types["category"]
    QuestionDeckHint.objects.create(
        question_id=question_id,
        deck=pitch_deck,
        hint={
            "type": "select",
            "value": [
                "Business Software",
                "IndustrialTech",
                "E-commerce",
                "Advertising & Marketing",
                "Hardware",
                "RetailTech",
                "ConstructionTech",
                "Web3",
                "EdTech",
                "Business Intelligence",
                "Cybersecurity",
                "HrTech",
                "Telecom & Communication",
                "Media & Entertainment",
                "FinTech",
                "MedTech",
                "Transport & Logistics",
                "Gaming",
                "FoodTech",
                "AI",
                "WorkTech",
                "Consumer Goods & Services",
                "Aero & SpaceTech",
                "Legal & RegTech",
                "Travel",
                "PropTech",
                "Energy",
                "GreenTech",
            ],
        },
    )

    req = requests.post(
        "https://rare-needles-lead.loca.lt/search",
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
    data = create_hints(pitch_deck.description, num)
    for el in data:
        question_type, question_id = data_types[el["type"]]
        QuestionDeckHint.objects.create(
            question_id=question_id,
            deck=pitch_deck,
            hint={"type": question_type, "value": el["value"]},
        )
