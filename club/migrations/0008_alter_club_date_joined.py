# Generated by Django 4.1.5 on 2023-02-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0007_club_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
