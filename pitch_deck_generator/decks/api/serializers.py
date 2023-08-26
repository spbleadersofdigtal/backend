from dateutil.parser import parse
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from pitch_deck_generator.decks.models import (
    PitchDeck,
    Question,
    QuestionAnswer,
    QuestionAnswerPhoto,
    QuestionDeckHint,
)


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
            question_id = (
                self.context["view"].kwargs["question_id"]
                if "question_id" in self.context["view"].kwargs
                else 1
            )
            if q := QuestionDeckHint.objects.filter(
                question_id=question_id,
                deck_id=self.context["view"].kwargs["deck_id"],
            ):
                return q.first().hint
            return {}
        return False

    @extend_schema_field(serializers.IntegerField)
    def get_next_id(self, obj):
        if q := Question.objects.filter(order=obj.order + 1):
            return q.first().id
        return 0

    class Meta:
        model = Question
        fields = ["id", "text", "hint", "required", "type", "params", "next_id"]


class AnswerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        file_fields = kwargs.pop("file_fields", None)
        super().__init__(*args, **kwargs)
        if file_fields:
            field_update_dict = {
                field: serializers.FileField(required=False, write_only=True)
                for field in file_fields
            }
            self.fields.update(**field_update_dict)

    file = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = QuestionAnswer
        fields = ["answer", "deck", "question", "file"]
        extra_kwargs = {
            "deck": {"read_only": True},
            "question": {"read_only": True},
        }

    def validate(self, data):
        answer = data["answer"]
        question = get_object_or_404(
            Question, id=self.context["view"].kwargs["question_id"]
        )
        deck = get_object_or_404(PitchDeck, id=self.context["view"].kwargs["deck_id"])
        question_type = question.type
        params = question.params if question.params else {}
        match question_type:
            case "text":
                if type(answer) is not str:
                    raise serializers.ValidationError("Incorrect type")
                if "max_length" in params:
                    if len(answer) > params["max_length"]:
                        raise serializers.ValidationError("Text is too long")
            case "number":
                if type(answer) is not str:
                    raise serializers.ValidationError("Incorrect type")
            case "text_array":
                if type(answer) is not list:
                    raise serializers.ValidationError("Incorrect type")

                if any([type(x) is not str for x in answer]):
                    raise serializers.ValidationError("Incorrect type")
            case "range":
                slug = params["slug"]
                if slug not in answer:
                    raise serializers.ValidationError("Value to found")
                if not isinstance(answer[slug], (int, float)):
                    raise serializers.ValidationError("Incorrect type")
                if not (params["min_value"] <= answer[slug] <= params["max_value"]):
                    raise serializers.ValidationError("Number is too big or too small")
            case "multiple_range":
                for slug in [x["slug"] for x in params["scrollbars"]]:
                    if slug not in answer:
                        raise serializers.ValidationError(f"Value {slug} to found")
                    if not isinstance(answer[slug], (int, float)):
                        raise serializers.ValidationError(f"Incorrect {slug} type")
                    if not (params["min_value"] <= answer[slug] <= params["max_value"]):
                        raise serializers.ValidationError(
                            f"Number is too big or too small for {slug}"
                        )
            case "select":
                if answer not in params["options"]:
                    raise serializers.ValidationError("No such option")
            case "date":
                try:
                    parse(answer)
                except ValueError:
                    raise serializers.ValidationError("Incorrect date type")
            case "photo":
                if answer:
                    raise serializers.ValidationError("Answer should be blank")

                if not data["file"]:
                    raise serializers.ValidationError("No file found")
            case "multiple_photo":
                if answer:
                    raise serializers.ValidationError("Answer should be blank")
                for key, value in data.items():
                    if isinstance(value, InMemoryUploadedFile):
                        if "_" not in key:
                            raise serializers.ValidationError(
                                "You should use file_num for file keys"
                            )
                        try:
                            int(key.split("_")[1])
                        except ValueError:
                            raise serializers.ValidationError(
                                "You should use file_num for file keys"
                            )

            case "photo_description":
                if not data["file"]:
                    raise serializers.ValidationError("No file found")
                if type(answer) is not str:
                    raise serializers.ValidationError("Incorrect type")
                if "max_length" in params:
                    if len(answer) > params["max_length"]:
                        raise serializers.ValidationError("Text is too long")
            case "multiple_photo_description":
                if type(answer) is not list:
                    raise serializers.ValidationError("Incorrect type")

                if any([type(x) is not str for x in answer]):
                    raise serializers.ValidationError("Incorrect type")

                len_f = 0

                for key, value in data.items():
                    if isinstance(value, TemporaryUploadedFile):
                        if "_" not in key:
                            raise serializers.ValidationError(
                                "You should use file_num for file keys"
                            )
                        try:
                            int(key.split("_")[1])
                        except ValueError:
                            raise serializers.ValidationError(
                                "You should use file_num for file keys"
                            )
                        len_f += 1
                if len_f != len(answer):
                    raise serializers.ValidationError(
                        "You should provide the same amount of answers in list as photos"
                    )

            case "multiple_link_description":
                if type(answer) is not dict:
                    raise serializers.ValidationError("Incorrect type")
                if any([type(x) is not str for x in answer.keys()]):
                    raise serializers.ValidationError("Incorrect type")
                if any([type(x) is not str for x in answer.values()]):
                    raise serializers.ValidationError("Incorrect type")

        data["question_id"] = question.id
        data["deck_id"] = deck.id
        return data

    def create(self, validated_data):
        q = QuestionAnswer.objects.get_or_create(
            deck_id=validated_data["deck_id"], question_id=validated_data["question_id"]
        )[0]
        q.answer = validated_data["answer"]
        q.save()

        s = [
            key
            for key, val in validated_data.items()
            if isinstance(val, TemporaryUploadedFile) and key != "file"
        ]
        if "file" in validated_data:
            QuestionAnswerPhoto.objects.create(answer=q, file=validated_data["file"])
        elif s:
            s.sort(key=lambda x: int(x.split("_")[1]))
            for key in s:
                QuestionAnswerPhoto.objects.create(answer=q, file=validated_data[key])
        return q
