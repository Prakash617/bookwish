# Generated by Django 4.1.5 on 2023-04-21 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0012_alter_event_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_link',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_link',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]