# Generated by Django 4.1.5 on 2023-03-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_merge_0009_alter_story_media_0010_merge_20230315_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postDescription',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
