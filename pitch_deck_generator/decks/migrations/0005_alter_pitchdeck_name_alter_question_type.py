# Generated by Django 4.2.4 on 2023-08-25 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("decks", "0004_alter_question_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pitchdeck",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("number", "Number"),
                    ("text_array", "Text Array"),
                    ("scroll", "Scroll"),
                    ("multiple_scroll", "Multiple Scroll"),
                    ("select", "Select"),
                    ("link", "Link"),
                    ("date", "Date"),
                    ("photo", "Photo"),
                    ("photo_description", "Photo Description"),
                    ("multiple_links", "Multiple Links"),
                ],
                max_length=17,
            ),
        ),
    ]
