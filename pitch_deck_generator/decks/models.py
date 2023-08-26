from django.db import models

from pitch_deck_generator.utils.choices import count_max_length


class PitchDeck(models.Model):
    # user put in info
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    questions = models.JSONField(default=dict, null=True, blank=True)

    # generated info
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    styles = models.FileField(upload_to="styles/", null=True, blank=True)
    presentation = models.FileField(upload_to="logos/", null=True, blank=True)
    meta_info = models.JSONField(default=dict, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated"]


class Question(models.Model):
    class QuestionType(models.TextChoices):
        text = "text"
        number = "number"
        text_array = "text_array", "text array"
        range = "range"
        multiple_range = "multiple_range", "multiple range"
        select = "select"
        link = "link"
        date = "date"
        multiple_date_description = (
            "multiple_date_description",
            "multiple date description",
        )
        photo = "photo"
        multiple_photo = "multiple_photo", "multiple photo"
        photo_description = "photo_description", "photo description"
        multiple_link_description = (
            "multiple_link_description",
            "multiple link description",
        )
        multiple_photo_description = (
            "multiple_photo_description",
            "multiple photo description",
        )
        multiple_links = "multiple_links", "multiple links"

    order = models.IntegerField(unique=True)
    text = models.CharField(max_length=300)
    type = models.CharField(
        choices=QuestionType.choices, max_length=count_max_length(QuestionType.choices)
    )
    hint = models.BooleanField(default=True)
    required = models.BooleanField(default=True)
    params = models.JSONField(blank=True, null=True)
    inner_tag = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return f"{self.order} - {self.text} - {self.type}"

    class Meta:
        ordering = ["order"]


class QuestionDeckHint(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    deck = models.ForeignKey(
        "PitchDeck", related_name="hints", on_delete=models.CASCADE
    )
    hint = models.JSONField(null=True, blank=True)


class QuestionAnswer(models.Model):
    deck = models.ForeignKey("PitchDeck", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.JSONField(default=dict)


class QuestionAnswerPhoto(models.Model):
    answer = models.ForeignKey(
        "QuestionAnswer", related_name="photos", on_delete=models.CASCADE
    )
    file = models.ImageField(upload_to="uploads/")
