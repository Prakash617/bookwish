# Generated by Django 4.1.5 on 2023-05-18 02:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event_app", "0037_alter_eventregistration_payment_info"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="event_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="event",
            name="price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
