# Generated by Django 4.1.5 on 2023-04-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0015_alter_health_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='record_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
