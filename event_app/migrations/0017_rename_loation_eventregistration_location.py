# Generated by Django 4.1.5 on 2023-04-21 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0016_eventregistration_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventregistration',
            old_name='loation',
            new_name='location',
        ),
    ]