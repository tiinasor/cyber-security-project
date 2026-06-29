from django.db import migrations
from django.utils import timezone


def seed_questions(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Choice = apps.get_model("polls", "Choice")

    seed_data = {
        "What's up?": ["Not much", "The sky", "Just hacking"],
        "What is your favorite color?": ["Red", "Green", "Blue"],
        "What is your favorite animal?": ["Cat", "Dog", "Horse"],
    }

    for question_text, choices in seed_data.items():
        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now(),
        )
        for choice_text in choices:
            Choice.objects.create(question=question, choice_text=choice_text)


def unseed_questions(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.filter(
        question_text__in=[
            "What's up?",
            "What is your favorite color?",
            "What is your favorite animal?",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_questions, unseed_questions),
    ]
