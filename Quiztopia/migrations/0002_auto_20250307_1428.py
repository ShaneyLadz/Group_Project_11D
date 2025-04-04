# Generated by Django 2.2.28 on 2025-03-07 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Quiztopia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('points', models.IntegerField(default=0)),
                ('quizzes_taken', models.IntegerField(default=0)),
                ('quizzes_created', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiztopia.UserProfile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
