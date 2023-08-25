from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from pitch_deck_generator.decks.api.serializers import (
    BasePitchDeckSerializer,
    PitchDeckSerializer,
    QuestionSerializer, HintSerializer,
)
from pitch_deck_generator.decks.models import PitchDeck


class ListDecksApiView(generics.ListCreateAPIView):
    queryset = PitchDeck.objects.all()
    serializer_class = BasePitchDeckSerializer


class RetrievePitchApiView(generics.RetrieveAPIView):
    serializer_class = PitchDeckSerializer

    def get_object(self):
        return get_object_or_404(PitchDeck, id=self.kwargs["id"])


class GetFirstQuestionApiView(generics.GenericAPIView):
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return Response()


class GetDeckQuestionApiView(generics.GenericAPIView):
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return Response()


class GetDeckQuestionHintApiView(generics.GenericAPIView):
    serializer_class = HintSerializer

    def get(self, request, *args, **kwargs):
        return Response()
