# Generated by Django 4.1.5 on 2023-02-21 08:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_alter_blog_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
