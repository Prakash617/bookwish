# Generated by Django 4.1.5 on 2023-03-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_rename_postimage_post_postmedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='media',
            field=models.FileField(blank=True, max_length=200, null=True, upload_to='story/'),
        ),
    ]