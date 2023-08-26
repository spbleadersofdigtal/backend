import datetime
from ast import literal_eval

import openai
from django.conf import settings

KEY = settings.OPENAI_KEY

description = """🍀 Что такое Pitch-Deck? Pitch-Deck представляет собой презентацию-тизер проекта/компании для
инвесторов, партнеров, журналистов и других заинтересованных лиц. Цель презентации - привлечение дополнительного
финансирования (инвестиций). Почему это проблема?

🍀 Проблема #1. Недостаток средств: Для многих стартапов ограниченные финансы создают преграду при разработке
качественного Pitch Deck. Отсутствие достаточных средств для найма профессиональных консультантов, дизайнеров и
копирайтеров, а также для проведения исследований рынка, может привести к созданию менее привлекательной и
малоинформативной презентации, что затрудняет привлечение инвестиций.

🍀 Проблема #2. Недостаток экспертизы: Проблемой для стартапов является недостаток экспертизы для проведения
необходимых исследований и корректного отражения их результатов в Pitch Deck. Не всегда у стартапов есть нужные
знания в области маркетинга, финансов и анализа рынка, что затрудняет создание убедительной и информативной
презентации для привлечения инвестиций.

🍀 Проблема #3. Недостаток времени Молодым компаниям для привлечения инвестиций требуется подготовить целый пакет
документов, одним из которых является Pitch Deck. Особенностью стартапов является сравнительного молодая и небольшая
команда, у которой чисто физически не хватает времени на разработку инвестиционных материалов, ведь они полностью
погружены в процесс разработки и улучшения продукта или сервиса.

🍀 ИДЕЯ: Основная идея кейса заключается в создании вспомогательного инструмента на основе ИИ, заточенного под
создание Pitch-Deck."""

names_prompt = """
По тексту ответь или предположи ответ на вопросы в следющем формате:
{
  "names": "Назови 5 имен проекта с данным описанием через запятую"
}
"""

prompts = [
    """
    По тексту ответь или предположи ответ на вопросы в следющем формате:
    {
      'users': 'Кто будет пользоваться продуктом',
      'problems': 'Какие проблемы решает продукт',
      'actuality': 'Продолжите предложение: Актуальность проблемы подтверждается тем фактом, что...',
      'solve': 'Как решаем эти проблемы',
      'works': 'Как работает решение',
    }
    """,
    """
    По тексту ответь или предположи ответ на вопросы в следющем формате:
    {
'awards': 'Когда проблема будет решена, какова будет ценность для ваших пользователей',
'money': 'На чем проект зарабатывает? сколько и за что ему платят клиенты',
'aims': Напиши 3 цели: на месяц, на полгода и год, формат: {'1': цель на месяц, '2': цель на полгода, '3': цель на год},
'investments_sold': 'На что потратить инвестиции под проект',
'financial_indicators': 'Напиши финансовые показатели проекта'
    }
    """,
    """
    По тексту ответь или предположи ответ на вопросы в следющем формате:
    {

      'achieve': 'Чего добьется команда после освоения инвестиций',
      'competitors_strength': 'Сильные стороны конкурентов',
      'competitors_low': 'Слабые стороны конкурентов',
      'advantages': 'Какие могут быть преимущества над конкурентами'
    }
    """,
]

openai.api_key = KEY

assertions = [
    [
        lambda data: "users" in data.keys(),
        lambda data: "problems" in data.keys(),
        lambda data: "actuality" in data.keys(),
        lambda data: "solve" in data.keys(),
        lambda data: "works" in data.keys(),
    ],
    [
        lambda data: "awards" in data.keys(),
        lambda data: "money" in data.keys(),
        lambda data: "aims" in data.keys(),
        lambda data: "investments_sold" in data.keys(),
        lambda data: "financial_indicators" in data.keys(),
    ],
    [
        lambda data: "achieve" in data.keys(),
        lambda data: "competitors_strength" in data.keys(),
        lambda data: "competitors_low" in data.keys(),
        lambda data: "advantages" in data.keys(),
    ],
]


def create_hints(description: str, stage: int):
    global prompts
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": description + "\n" + prompts[stage]}],
    )
    content = literal_eval(chat_completion.choices[0].message.content)
    for assertion_statement in assertions[stage]:
        assert assertion_statement(content)

    if stage == 1:
        content["aims"] = [
            {
                "aim": content["aims"]["1"],
                "date": (
                    datetime.datetime.now() + datetime.timedelta(days=30)
                ).isoformat(),
            },
            {
                "aim": content["aims"]["2"],
                "date": (
                    datetime.datetime.now() + datetime.timedelta(days=180)
                ).isoformat(),
            },
            {
                "aim": content["aims"]["3"],
                "date": (
                    datetime.datetime.now() + datetime.timedelta(days=365)
                ).isoformat(),
            },
        ]
    result = []
    for key, value in content.items():
        result.append({"type": key, "value": value})
    return result


def create_name_hint(description: str):
    global names_prompt
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": description + "\n" + names_prompt}],
    )
    answer = literal_eval(chat_completion.choices[0].message.content)["names"].split(
        ", "
    )
    assert len(answer) == 5
    return {"type": "names", "value": answer}


# print(create_name_hint(description))
# print(create_hints(description, 0))
# print(create_hints(description, 1))
# print(create_hints(description, 2))
