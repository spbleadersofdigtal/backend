from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from pitch_deck_generator.decks.api.serializers import (
    AnswerSerializer,
    BasePitchDeckSerializer,
    HintSerializer,
    PdfToPPTXSerializer,
    PitchDeckPresentationSerializer,
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


class GetDeckPresentationDataApiView(generics.GenericAPIView):
    queryset = PitchDeck.objects.none()
    serializer_class = PitchDeckPresentationSerializer

    structure = {
        1: ["names", "type"],
        2: ["problems"],
        3: ["actuality", "awards"],
        4: ["solve", "works"],
        5: ["market_values", "users"],
        6: ["competitors", "competitors_strength", "competitors_low", "advantages"],
        7: ["money", "finance_model"],
        8: ["how_much_investments", "financial_indicators", "users_metrics"],
        9: ["your_role", "your_teammates", "past_investors"],
        10: ["how_much_investments", "time_to_spend", "investments_sold"],
        11: ["company_value", "future_value", "time_to_spend"],
        12: ["aims"],
        13: ["images"],
    }

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(
            PitchDeck,
            id=self.kwargs["deck_id"],
        )
        re_data = {
            "deck": BasePitchDeckSerializer().to_representation(deck),
        }
        resp = []
        data = deck.questions
        for slide, tags in self.structure.items():
            slide_data = {"slide": slide, "data": []}
            for tag in tags:
                b_data = {}
                if tag in data:
                    if "answer" in data[tag]:
                        b_data["answer"] = data[tag]["answer"]
                    if "photos" in data[tag]:
                        b_data["photos"] = data[tag]["photos"]

                slide_data["data"].append({"slug": tag, **b_data})
            resp.append(slide_data)
        re_data["slides"] = resp
        return Response(re_data)


class ConvertPdfToPPTXApiView(generics.CreateAPIView):
    serializer_class = PdfToPPTXSerializer
    parser_classes = [FormParser, MultiPartParser]
