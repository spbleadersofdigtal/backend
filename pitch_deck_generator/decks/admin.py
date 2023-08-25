from django.contrib import admin

from pitch_deck_generator.decks.models import Question, PitchDeck

admin.site.register(PitchDeck)
admin.site.register(Question)
