# Generated by Django 4.1.5 on 2023-04-29 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0028_delete_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventwrittenquestions',
            name='answers',
        ),
    ]
