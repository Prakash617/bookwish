# Generated by Django 4.1.5 on 2023-04-29 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0027_eventwrittenquestions_asked_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Questions',
        ),
    ]
