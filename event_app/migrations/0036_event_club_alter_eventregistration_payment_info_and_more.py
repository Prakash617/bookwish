# Generated by Django 4.1.5 on 2023-05-17 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import event_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0017_alter_club_club_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("event_app", "0035_eventcalender"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="club",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="club.club",
            ),
        ),
        migrations.AlterField(
            model_name="eventregistration",
            name="payment_info",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="PaymentInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("Esewa", "Esewa"),
                            ("FonePay", "Fonepay"),
                            ("Bank", "Bank"),
                        ],
                        default="ESEWA",
                        max_length=9999,
                    ),
                ),
                (
                    "details",
                    models.JSONField(
                        blank=True, default=event_app.models.data, null=True
                    ),
                ),
                (
                    "remarks",
                    models.JSONField(
                        blank=True, default=event_app.models.data, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
