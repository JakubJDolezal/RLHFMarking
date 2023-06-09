# Generated by Django 4.2 on 2023-06-04 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Marking", "0002_response_question_alter_response_score_and_more"),
    ]

    operations = [
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
                ("text", models.TextField(default="Default question")),
            ],
        ),
        migrations.AlterField(
            model_name="response",
            name="text",
            field=models.TextField(default="Default response"),
        ),
        migrations.AlterField(
            model_name="response",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Marking.question"
            ),
        ),
    ]
