# Generated by Django 4.1.5 on 2023-02-23 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0004_rename_deficit_health_bellysize_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='record_date',
            field=models.DateField(null=True),
        ),
    ]