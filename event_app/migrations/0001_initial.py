# Generated by Django 4.1.5 on 2023-02-12 16:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=999)),
                ('event_start_time', models.TimeField()),
                ('event_end_time', models.TimeField()),
                ('event_start_date', models.DateField()),
                ('event_end_date', models.DateField()),
                ('event_topic', models.CharField(max_length=999)),
                ('event_location', models.CharField(max_length=999)),
                ('picture', models.URLField()),
                ('description', models.CharField(max_length=999)),
                ('registration_link', models.URLField()),
                ('event_link', models.URLField()),
                ('event_type', models.CharField(max_length=999)),
                ('is_paid', models.BooleanField(default='False')),
                ('participant_numbers', models.IntegerField()),
                ('event_uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=999)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=999)),
                ('loation', models.CharField(max_length=999)),
                ('attended', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('payment_info', models.JSONField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Event_registration', to='event_app.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=999)),
                ('option1', models.CharField(max_length=999)),
                ('option2', models.CharField(max_length=999)),
                ('option3', models.CharField(max_length=999)),
                ('option4', models.CharField(max_length=999)),
                ('correct_answer', models.CharField(max_length=999)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Event_question', to='event_app.event')),
            ],
        ),
    ]