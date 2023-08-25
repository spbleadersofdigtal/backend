from django.urls import path

from pitch_deck_generator.tickets.api.views import RetrieveTicketSerializer

urlpatterns = [
    path("<str:uuid>", RetrieveTicketSerializer.as_view(), name="ticket"),
]
