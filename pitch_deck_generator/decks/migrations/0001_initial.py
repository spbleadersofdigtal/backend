# Generated by Django 4.2.4 on 2023-08-25 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PitchDeck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("description", models.TextField()),
                ("questions", models.JSONField(blank=True, default=dict, null=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="logos/")),
                (
                    "styles",
                    models.FileField(blank=True, null=True, upload_to="styles/"),
                ),
                (
                    "presentation",
                    models.FileField(blank=True, null=True, upload_to="logos/"),
                ),
                ("meta_info", models.JSONField(blank=True, default=dict, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated"],
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.IntegerField(unique=True)),
                ("text", models.CharField(max_length=300)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("scroll", "Scroll"),
                            ("select", "Select"),
                            ("link", "Link"),
                            ("time", "Time"),
                            ("photo", "Photo"),
                            ("multiple_links", "Multiple Links"),
                        ],
                        max_length=14,
                    ),
                ),
                ("hint", models.BooleanField(default=True)),
                ("required", models.BooleanField(default=True)),
                ("condition", models.CharField(blank=True, max_length=250, null=True)),
                ("params", models.JSONField(blank=True, null=True)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="QuestionAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deck", models.FloatField(verbose_name="PitchDeck")),
                ("answer", models.JSONField(default={"answer": "", "type": "text"})),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="decks.question"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionDeckHint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hint", models.CharField(max_length=500)),
                (
                    "deck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hints",
                        to="decks.pitchdeck",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="decks.question"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionAnswerPhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.ImageField(upload_to="uploads/")),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="decks.questionanswer",
                    ),
                ),
            ],
        ),
    ]
