# Generated by Django 4.1.5 on 2023-05-18 02:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("event_app", "0038_event_event_paid_event_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="event_paid",
        ),
    ]
