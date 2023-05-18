# Generated by Django 4.1.5 on 2023-04-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_consultationrequest_courses_recommendedarticles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='about_mission',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='about_us',
            field=models.TextField(blank=True, max_length=99999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='about_vision',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='consultation_request',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='founder_bio',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='helpful_forms',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='link_and_resources',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='privacy_policy',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='services_page',
            field=models.TextField(blank=True, max_length=9999),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='terms_of_service',
            field=models.TextField(blank=True, max_length=9999),
        ),
    ]
