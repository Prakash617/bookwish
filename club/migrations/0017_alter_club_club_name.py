# Generated by Django 4.1.5 on 2023-04-11 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0016_alter_health_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]