# Generated by Django 2.2.28 on 2025-03-19 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiztopia', '0003_quiz_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='slug',
            new_name='category_slug',
        ),
    ]
