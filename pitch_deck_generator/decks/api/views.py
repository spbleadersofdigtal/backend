from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from pitch_deck_generator.decks.api.serializers import (
    AnswerSerializer,
    BasePitchDeckSerializer,
    HintSerializer,
    PitchDeckSerializer,
    QuestionSerializer,
)
from pitch_deck_generator.decks.models import PitchDeck, Question, QuestionDeckHint


class ListDecksApiView(generics.ListCreateAPIView):
    queryset = PitchDeck.objects.all()
    serializer_class = BasePitchDeckSerializer


class RetrievePitchApiView(generics.RetrieveAPIView):
    serializer_class = PitchDeckSerializer

    def get_object(self):
        return get_object_or_404(PitchDeck, id=self.kwargs["id"])


class GetFirstQuestionApiView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        return Question.objects.get(order=1)


class GetDeckQuestionApiView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs["question_id"])


class CreateQuestionAnswerApiView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        # main thing starts
        file_fields = list(request.FILES.keys())  # list to be passed to the serializer
        serializer = self.get_serializer(data=request.data, file_fields=file_fields)
        # main thing ends

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class GetDeckQuestionHintApiView(generics.GenericAPIView):
    serializer_class = HintSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request, *args, **kwargs):
        hint = get_object_or_404(
            QuestionDeckHint,
            question_id=self.kwargs["question_id"],
            deck_id=self.kwargs["deck_id"],
        )
        data = hint.hint
        if data:
            return Response(data)
        return Response(status=404)
