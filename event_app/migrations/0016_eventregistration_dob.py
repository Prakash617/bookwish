# Generated by Django 4.1.5 on 2023-04-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0015_remove_eventregistration_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='dob',
            field=models.DateField(null=True),
            preserve_default=False,
        ),
    ]
