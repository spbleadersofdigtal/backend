from django.urls import path

from pitch_deck_generator.decks.api.views import (
    ListDecksApiView,
    RetrievePitchApiView,
    GetFirstQuestionApiView,
    GetDeckQuestionApiView,
    GetDeckQuestionHintApiView,
)

app_name = "decks"

urlpatterns = [
    path("", ListDecksApiView.as_view()),
    path("<int:id>", RetrievePitchApiView.as_view()),
    path("question/<int:deck_id>", GetFirstQuestionApiView.as_view()),
    path("question/<int:deck_id>/<int:question_id>", GetDeckQuestionApiView.as_view()),
    path("hint/<int:deck_id>/<int:question_id>", GetDeckQuestionHintApiView.as_view()),
]
