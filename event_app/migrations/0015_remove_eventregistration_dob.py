# Generated by Django 4.1.5 on 2023-04-21 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0014_eventregistration_dob_eventregistration_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventregistration',
            name='dob',
        ),
    ]
