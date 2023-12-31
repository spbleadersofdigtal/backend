# Generated by Django 4.2.4 on 2023-08-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("decks", "0002_rename_condition_question_inner_tag_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("text_array", "Text Array"),
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
        migrations.AlterField(
            model_name="questiondeckhint",
            name="hint",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
