from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from pitch_deck_generator.decks.models import PitchDeck, Question, QuestionDeckHint


class BasePitchDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchDeck
        fields = ["id", "name", "description", "logo", "created", "updated"]
        extra_kwargs = {
            "id": {"read_only": True},
            "logo": {"read_only": True},
            "name": {"read_only": True},
            "created": {"read_only": True},
            "updated": {"read_only": True},
        }


class PitchDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchDeck
        fields = "__all__"


class HintSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Question.QuestionType.choices)
    value = serializers.JSONField()


class QuestionSerializer(serializers.ModelSerializer):
    hint = serializers.SerializerMethodField(method_name="get_hint")
    next_id = serializers.SerializerMethodField(method_name="get_next_id")

    @extend_schema_field(HintSerializer)
    def get_hint(self, obj):
        if obj.hint:
            if q := QuestionDeckHint.objects.filter(
                question_id=self.context["kwargs"]["question"],
                deck_id=self.context["kwargs"]["deck"],
            ):
                return q.first().hint
            return ""
        return False

    @extend_schema_field(serializers.IntegerField)
    def get_next_id(self, obj):
        if q := Question.objects.filter(order=obj.order + 1):
            return q.first().id
        return 0

    class Meta:
        model = Question
        fields = ["id", "text", "hint", "required", "params", "next_id"]
