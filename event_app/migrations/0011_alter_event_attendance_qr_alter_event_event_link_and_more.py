# Generated by Django 4.1.5 on 2023-04-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0010_event_attendance_link_event_attendance_qr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendance_qr',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=999),
        ),
    ]
