from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("ticket/", include("pitch_deck_generator.tickets.api.urls")),
    path("decks/", include("pitch_deck_generator.decks.api.urls")),
]
