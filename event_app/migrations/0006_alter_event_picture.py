# Generated by Django 4.1.5 on 2023-03-23 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0005_alter_event_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(max_length=99, upload_to='event'),
        ),
    ]
