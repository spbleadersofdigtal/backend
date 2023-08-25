from rest_framework import serializers

from pitch_deck_generator.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    current = serializers.IntegerField()

    class Meta:
        model = Ticket
        fields = ["name", "current", "max", "next"]
