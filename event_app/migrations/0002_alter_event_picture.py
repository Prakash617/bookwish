# Generated by Django 4.1.5 on 2023-03-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(upload_to='event/'),
        ),
    ]