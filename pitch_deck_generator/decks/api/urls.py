from django.urls import path

from pitch_deck_generator.decks.api.views import (
    CreateQuestionAnswerApiView,
    GetDeckQuestionApiView,
    GetDeckQuestionHintApiView,
    GetFirstQuestionApiView,
    ListDecksApiView,
    RetrievePitchApiView,
)

app_name = "decks"

urlpatterns = [
    path("", ListDecksApiView.as_view()),
    path("<int:id>", RetrievePitchApiView.as_view()),
    path("question/<int:deck_id>", GetFirstQuestionApiView.as_view()),
    path("question/<int:deck_id>/<int:question_id>", GetDeckQuestionApiView.as_view()),
    path(
        "question/<int:deck_id>/<int:question_id>/",
        CreateQuestionAnswerApiView.as_view(),
    ),
    path("hint/<int:deck_id>/<int:question_id>", GetDeckQuestionHintApiView.as_view()),
]
