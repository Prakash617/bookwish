# Generated by Django 4.1.5 on 2023-03-22 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_alter_basicinfo_founder_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicinfo',
            name='link_and_resources',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='privacy_policy',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='terms_of_service',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]